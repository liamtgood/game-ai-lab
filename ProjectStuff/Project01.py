from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))
import json
import random
import os
from util.llm_utils import run_console_chat, tool_tracker, TemplateChat
import glob
import time
from typing import List, Dict, Any

# Vector database, embedding, and text processing
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter


import ollama
import numpy as np

# Utility imports
import pandas as pd

TRADER_KEYWORDS = ["trader", "merchant", "shopkeeper", "buy", "sell", "trade"]
# Trader interaction
trader_file = 'ProjectStuff/trader.json'
if not os.path.exists(trader_file):
    print(f"Error: Trader file not found at {trader_file}")
# beauty of Python
@tool_tracker
def process_function_call(function_call):
    name = function_call.name
    args = function_call.arguments

    return globals()[name](**args)

#skill roll for
def roll_for(skill, dc, player):
    n_dice = 1
    sides = 20
    if dc is None:
        dc = 10  # Default DC if not provided
    roll = sum([random.randint(1, sides) for _ in range(n_dice)])
    if roll >= int(dc):
        return f'{player} rolled {roll} for {skill} and succeeded!'
    else:
        return f'{player} rolled {roll} for {skill} and failed!'
    
#template to interact with a trader
def interact_with_trader(trader_file):
    with open(trader_file, 'r') as file:
        trader_data = json.load(file)

    model = trader_data.get("model", "default_model")
    options = trader_data.get("options", {})
    messages = trader_data.get("messages", [])

    # Instantiate the chat
    chat = TemplateChat(model=model, options=options, messages=messages)

    # Define ending keywords or phrases
    END_KEYWORDS = ["thank you for your purchase", "farewell", "goodbye", "come again", "end the interaction"]

    while True:
        response = chat.completion()
        print(f"Trader: {response}")

        # Check for any ending keyword in the response (case-insensitive)
        if any(kw in response.lower() for kw in END_KEYWORDS):
            break

        user_input = input("You (to trader): ")
        messages.append({"role": "user", "content": user_input})
        chat = TemplateChat(model=model, options=options, messages=messages)

    response = chat.completion()

    # Display the response from the trader
    print(f"Trader response: {response}")  # Debugging statement
    return response


#def handle_trader_interaction(trader_file, regular_model, regular_options, regular_messages):
def handle_trader_interaction(trader_file, *_):
    try:
        interact_with_trader(trader_file)
    except Exception as e:
        print(f"Error during trader interaction: {e}")
#handles user response
def process_response(self, response):
    if response.message.tool_calls:
        tool_name = response.message.tool_calls[0].function.name
        tool_args = response.message.tool_calls[0].function.arguments

        # Handle only the 'roll_for' tool
        if tool_name == "roll_for":
            self.messages.append({
                'role': 'tool',
                'name': tool_name,
                'arguments': tool_args,
                'content': process_function_call(response.message.tool_calls[0].function)
            })
            response = self.completion()
    return response

###RAG
class OllamaEmbeddingFunction:
    """Custom embedding function that uses Ollama for embeddings"""
    
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Ollama"""
        
        #get the response
        response = ollama.embed(model=self.model_name, input=input)
            
        #return the embedidngs from the response
        return response["embeddings"]

        #pass


def load_documents(data_dir: str) -> Dict[str, str]:
    """
    Load text documents from a directory
    """
    documents = {}
    for file_path in glob.glob(os.path.join(data_dir, "*.txt")):
        with open(file_path, 'r') as file:
            content = file.read()
            documents[os.path.basename(file_path)] = content
    
    print(f"Loaded {len(documents)} documents from {data_dir}")
    return documents


def chunk_documents(documents: Dict[str, str], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Split documents into smaller chunks for embedding,
    using LangChain's RecursiveCharacterTextSplitter
    """
    chunked_documents = []
    
    # Create the chunker with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    for doc_name, content in documents.items():
        # Apply the chunker to the document text
        
        chunks = text_splitter.split_text(content)
        
        for i, chunk in enumerate(chunks):
            chunked_documents.append({
                "id": f"{doc_name}_chunk_{i}",
                "text": chunk,
                "metadata": {"source": doc_name, "chunk": i}
          })
    
    print(f"Created {len(chunked_documents)} chunks from {len(documents)} documents")
    return chunked_documents


def setup_chroma_db(chunks: List[Dict[str, Any]], collection_name: str = "dnd_knowledge", use_ollama_embeddings: bool = True, ollama_model: str = "nomic-embed-text") -> chromadb.Collection:
    """
    Set up ChromaDB with document chunks
    """
    # Initialize ChromaDB Ephemeral client
    client = chromadb.Client()
    # Initialize ChromaDB Persistent client
    #client = chromadb.PersistentClient(path="/path/to/save/to")
    
    # Create embedding function
    # Use custom Ollama embedding function
    embedding_function = OllamaEmbeddingFunction(model_name=ollama_model)
    print(f"Using Ollama for embeddings with model: {ollama_model}")
    
    # Create or get collection
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    
    # Add documents to collection
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks]
    )
    
    print(f"Added {len(chunks)} chunks to ChromaDB collection '{collection_name}'")
    return collection

#here
def retrieve_context(collection: chromadb.Collection, query: str, n_results: int = 3) -> List[str]:
    """
    Retrieve relevant context from ChromaDB based on the query
    """
    #query the results//
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    #Extract text chunks and ensure they are strings
    context_chunks = [doc if isinstance(doc, str) else str(doc) for doc in results["documents"]]
    print(f"Retrieved {len(context_chunks)} context chunks for the query: '{query}'")
    #return chunchs
    return context_chunks


def generate_response(query: str, contexts: List[str], model: str = "mistral:latest") -> str:
    """
    Generate a response using Ollama LLM with the retrieved context
    """
    # Create prompt with context
    context_text = "\n\n".join(contexts)
    
    prompt = f"""You are a helpful assistant for Dungeons & Dragons players.
    Use the following information to answer the question.
    
    Context:
    {context_text}
    
    Question: {query}
    
    Answer:"""
    
    response = ollama.generate(
        model=model,
        prompt=prompt,
    )
    
    return response["response"]

#####rag








run_console_chat(template_file='ProjectStuff/game.json',
                 process_response=process_response)

# Regular model configuration
regular_model = "llama3.2"
regular_options = {"temperature": 1.0, "max_tokens": 150}
regular_messages = [{"role": "system", "content": "You are a helpful assistant."}]
# Set embedding and LLM models
embedding_model = "nomic-embed-text"  # Change to your preferred embedding model
llm_model = "llama3.2:latest"  # Change to your preferred LLM model

# 1. Load documents
data_dir = "ProjectStuff/Lore.txt"
documents = load_documents(data_dir)

# 2. Chunk documents using ChromaDB chunker
chunks = chunk_documents(documents)

# 3. Set up ChromaDB with Ollama embeddings
collection = setup_chroma_db(
    chunks, 
    ollama_model=embedding_model
)
    
#main loop
while True:

    # Get user input
    user_input = input("You: ").strip()

    # Exit condition
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # Check if the user input contains any trader keywords
    if any(keyword in user_input for keyword in TRADER_KEYWORDS):
        chat = handle_trader_interaction(trader_file, regular_model, regular_options, regular_messages)
        continue  # Go back to the loop after trader interaction

    # Retrieve relevant lore chunks
    retrieved_chunks = retrieve_context(collection, user_input)

    if retrieved_chunks:
        print(f"Debug: Retrieved {len(retrieved_chunks)} chunks from lore.")  # Debugging statement

        # Generate a response using the retrieved context
        response = generate_response(user_input, retrieved_chunks, model=llm_model)
    else:
        # If no relevant lore is found, generate a response without context
        response = generate_response(user_input, [], model=llm_model)

    # Display the response
    print(f"Assistant: {response}")
