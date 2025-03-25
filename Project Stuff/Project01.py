from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import run_console_chat, tool_tracker, TemplateChat, pretty_stringify_chat, ollama_seed as seed


#model 
sign_your_name = 'Liam Good'
model = 'llama3.2'
messages = [{'role': 'system', 'content': 'You should have emotions like a human being and be able to convey those emotions in your responses.\
                                You should be a very good d&d dungeon master. You will use DnD 5th Edition. \
                                As the dungeon master you will first start by helping the player create their character. \
                                ensure to include all the character classes for dnd 5th edition for the player to select in character creation.\
                                After character creation the adventure will begin. Make sure the adverture is very creative. '
                                }]
#asks if the player is ready to begin playing
messages.append({'role': 'assistant', 'content': 'Are you ready to begin your adventure? '})
options = {'temperature': 0.5, 'max_tokens': 10}
response = chat(model = model, messages = messages, stream = False, options = options)

# create the player character - name, class, stats, starting items
messages.append({'role':'assistant','content':'Let\'s begin Character Creation! Chose A class: \n -Fighter \n -Wizard \n -Rogue \n -Cleric \n -Bard\n'})
options = {'temperature': 0.5, 'max_tokens': 10}
response = chat(model = model, messages = messages, stream = False, options = options)



# once player selects a class use rag to describe that classes abilities

# #store all this information somewhere


# starts adventure
options |= {'seed': seed(sign_your_name)}
# Chat loop
while True:
  response = chat(model=model, messages=messages, stream=False, options=options)
  # chat system
  messages.append({'role': 'assistant', 'content': response.message.content})
  print(f'Agent: {response.message.content}')
  message = {'role': 'user', 'content': input('You: ')}
  messages.append(message)
  # 
  if messages[-1]['content'] == '/exit':
    break
  


