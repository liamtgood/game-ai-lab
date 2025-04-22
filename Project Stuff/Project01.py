from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))
import json
import random
from util.llm_utils import run_console_chat, tool_tracker, TemplateChat

# beauty of Python
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

def interact_with_trader(trader_file):
    # Load the trader configuration from trader.json
    with open(trader_file, 'r') as file:
        trader_data = json.load(file)

    # Extract model, options, and messages
    model = trader_data.get("model", "default_model")
    options = trader_data.get("options", {})
    messages = trader_data.get("messages", [])

    # Use TemplateChat or another LLM utility to simulate the interaction
    chat = TemplateChat(model=model, options=options, messages=messages)
    response = chat.completion()

    # Display the response from the trader
    print(response)
    return response

def handle_trader_interaction(trader_file, regular_model, regular_options, regular_messages):
    print("Entering trader interaction...")
    
    # Call the trader chat
    interact_with_trader(trader_file)

    print("Exiting trader interaction...")
    # Return to the regular model
    chat = TemplateChat(model=regular_model, options=regular_options, messages=regular_messages)
    return chat

def process_response(self, response):
    if response.message.tool_calls:
        tool_name = response.message.tool_calls[0].function.name

        # Handle only the 'roll_for' tool
        if tool_name == "roll_for":
            self.messages.append({
                'role': 'tool',
                'name': tool_name,
                'arguments': response.message.tool_calls[0].function.arguments,
                'content': process_function_call(response.message.tool_calls[0].function)
            })
            response = self.completion()
    return response


run_console_chat(template_file='Project Stuff\_roll_for.json',
                 process_response=process_response)

# Regular model configuration
regular_model = "llama3.2"
regular_options = {"temperature": 0.7, "max_tokens": 150}
regular_messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Trader interaction
trader_file = 'trader.json'
chat = handle_trader_interaction(trader_file, regular_model, regular_options, regular_messages)

# Continue with the regular chat
response = chat.completion()
print(response)
