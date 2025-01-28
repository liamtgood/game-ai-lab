from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Add you code below
sign_your_name = 'Liam Good'
model = 'llama3.2'
messages = [{'role': 'system', 'content': 'You should have emotions like a human being \
                                 and be able to convey those emotions in your responses. You should be a dungeon master in DND. \
                                As a dungeon master you need to do everything that a dungeon master would be asked to do. \
                                You need to help create characters, and create the adventure. You need to start off every adventure with creating characters. \
                                once the character is created then you may begin the adventure. We will be using DnD 5th Edition for our game. You can use the official dnd 5th edition \
                                hand book for character creation and for constructing the adventure'}]
options = {'temperature': 0.5, 'max_tokens': 100}
response = chat(model = model, messages = messages, stream = False, options = options)

# But before here.

options |= {'seed': seed(sign_your_name)}
# Chat loop
while True:
  response = chat(model=model, messages=messages, stream=False, options=options)
  # Add your code below
  messages.append({'role': 'assistant', 'content': response.message.content})
  print(f'Agent: {response.message.content}')
  message = {'role': 'user', 'content': input('You: ')}
  messages.append(message)
  # But before here.
  if messages[-1]['content'] == '/exit':
    break

# Save chat
with open(Path('lab03/attempts.txt'), 'a') as f:
  file_string  = ''
  file_string +=       '-------------------------NEW ATTEMPT-------------------------\n\n\n'
  file_string += f'Model: {model}\n'
  file_string += f'Options: {options}\n'
  file_string += pretty_stringify_chat(messages)
  file_string += '\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n'
  f.write(file_string)

