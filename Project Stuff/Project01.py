from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

import random
from util.llm_utils import run_console_chat, tool_tracker, TemplateChat, pretty_stringify_chat, ollama_seed as seed


@tool_tracker
def process_function_call(function_call):
    name = function_call.name
    args = function_call.arguments

    return globals()[name](**args)

def roll_for(skill, dc, player):
    n_dice = 1
    sides = 20
    roll = sum([random.randint(1, sides) for _ in range(n_dice)])
    if roll >= int(dc):
        return f'{player} rolled {roll} for {skill} and succeeded!'
    else:
        return f'{player} rolled {roll} for {skill} and failed!'

def process_response(self, response):
    # Fill out this function to process the response from the LLM
    # and make the function call 
    #chat = TemplateChat.from_file(self)
    #response = chat.completion(**{'ask': 'Roll for athletic skill to see if the player can pass over the ravine'})

    #defaultdict(<class 'list'>, {'process_function_call_calls': [{'name': 'process_function_call', 'args': (Function(name='roll_for', arguments={'dc': 5, 'player': 'adventurer', 'skill': 'Athletics'}),), 'kwargs': {}, 'result': 'adventurer rolled 7 for Athletics and succeeded!'}]}) 

    if response.message.tool_calls:
        self.messages.append({'role': 'tool',
                          'name': response.message.tool_calls[0].function.name, 
                          'arguments': response.message.tool_calls[0].function.arguments,
                          'content': process_function_call(response.message.tool_calls[0].function)
                         })
        response = self.completion()
    return response


run_console_chat(template_file='Project Stuff/dice.json',
                 process_response=process_response)


# once player selects a class use rag to describe that classes abilities





