# Project Report

## 1. Core System Functionalities
- The foundational AI system operates flawlessly, effectively managing the Dungeons and Dragons (DnD) scenarios it initiates. It begins with character creation and seamlessly transitions into the adventure.  
- The model is specifically designed to act as a dungeon master, adhering strictly to DnD rules.  
- It successfully demonstrates Learning Outcome 1 (LO1) by leveraging AI to generate the core game narrative and exemplifies Learning Outcome 3 (LO3) through its modular design and robust functionality.  

## 2. Prompt Engineering and Model Parameter Optimization
- A temperature setting of 1.0 was employed to encourage creative and diverse storytelling, as lower values led to repetitive and predictable narratives.  
- The maximum token limit was set to 150, ensuring concise yet engaging interactions.  
- Initial prompts were meticulously crafted to enhance the model's performance as a D&D dungeon master. These prompts outlined the game's structure, including how adventures should begin and how the model should respond to player actions.  
- The model consistently adhered to user instructions while incorporating contextual elements, delivering a dynamic and immersive gameplay experience.  

## 3. Tool Integration
- A dice-rolling tool was implemented to seamlessly integrate with the AI model. This tool is invoked whenever a dice roll is required, dynamically influencing the model's responses.  
- The tool operates with three parameters: the skill being tested, the difficulty class (DC) representing the target number to beat, and the player for whom the roll is being made. It returns the roll result and indicates success or failure, adding an interactive and randomized element to the gameplay.  

## 4. Narrative Planning and Coherence
- The model employs a chain-of-thought approach to maintain narrative coherence and ensure the story remains engaging. It effectively informs players about the characters they are interacting with and clearly indicates when someone is speaking.  
- While the model may occasionally deviate from the storyline when presented with unrelated input, it generally allows players to seamlessly return to the original narrative, preserving the flow of the adventure.  

## 5. Retrieval-Augmented Generation (RAG)
- Retrieval-Augmented Generation (RAG) is utilized to enrich the player's journey by recalling key events and details from earlier in the story.  
- RAG also dynamically generates items for players to discover during their adventure. Each item is accompanied by detailed explanations, enabling the model to understand their functionality and seamlessly integrate them into the narrative.  

## 6. Additional Features and Innovations
- A specialized Trader template enhances gameplay by facilitating interactions with traders. When specific keywords are detected, the template is activated, allowing for a focused trading experience. Once the interaction concludes, the model seamlessly returns to the main narrative.  
- The template leverages the `interact_with_trader()` and `handle_trader_interaction()` functions to manage these interactions. Keywords for entering and exiting the template are intuitive, ensuring a smooth and natural player experience.  
