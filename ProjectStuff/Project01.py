from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))
import json
import random
import os
from util.llm_utils import run_console_chat, tool_tracker, TemplateChat

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


run_console_chat(template_file='ProjectStuff/game.json',
                 process_response=process_response)

# Regular model configuration
regular_model = "llama3.2"
regular_options = {"temperature": 1.0, "max_tokens": 150}
regular_messages = [{"role": "system", "content": "You are a helpful assistant."}]


while True:
    # Get user input
    user_input = input("You: ").lower()

    # Check if the user input contains any trader keywords
    if any(keyword in user_input for keyword in TRADER_KEYWORDS):
        chat = handle_trader_interaction(trader_file, regular_model, regular_options, regular_messages)
        continue  # Go back to the loop after trader interaction

    # Otherwise, process the regular chat
    regular_messages.append({"role": "user", "content": user_input})
    chat = TemplateChat(model=regular_model, options=regular_options, messages=regular_messages)
    response = chat.completion()
    print(f"Assistant: {response}")
