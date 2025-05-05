# Ideas

## First the model starts by having you create your character
- Choose a class
- use rag implemtentation to give the player an insight into all the characters
- choose a name
- Get assigned random stats
- get starting weapons
- all of this is stored somewhere so the model can get this information

## Adventure Begins
- The model will give the player different prompts, the player will then tell the model what they want to do
- /*{
  "model": "llama3.2",
  "options": {
    "temperature": 0,
    "sign": "Liam Good"
  },
  "messages": [{"role": "system", "content": "You should have emotions like a human being and be able to convey those emotions in your responses. You should be a very good d&d dungeon master. You will use DnD 5th Edition. As the dungeon master you will first start by helping the player create their character. ensure to include all the character classes for dnd 5th edition for the player to select in character creation. After character creation explain what the player's character does. Then the adventure will begin. Make sure the adverture is very creative.  When you need to, you can use the 'roll_for' tool/function when you want the player to pass a skill check for something that they want to accomplish in the game. You will decide what activities need a skill check. You may not need to do skill checks for trivial things that a player may want to do, but the player may ask for a skill check. You will use 'roll_for' tool to check if the user passes a skill check. Only use tools if a skill check is needed. Sometimes you do not need to do the skill check"}
    ,{"role": "assistant", "content": ""}],
    "tools": [
      {
        "type": "function",
        "function":{
          "name": "roll_for",
          "description":"Rolls for different skills in dnd",
          "parameters":{
            "type":"object",
            "properties":{"skill":{"type":"string"},"dc":{"type":"integer"},"player":{"type":"string"}}
          }
        }
      }
    ]
}*/