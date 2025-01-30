# Prompt Engineering Process


# Reflection
To start I was just getting a hang of the system and how it worked. So for the first attempt I just used the demo and asked it to make a dnd game for me. It did a decent job at it but I think it can do better. Next I made it so after you exit there is no message after and it immidietly exits. 

For the next attempt I changed the initial message given to the model. Here I told the model it was a dungeon master for dnd. I gave it some basic information on what to do. Also here, my first message was just "let's begin" and the model immidietly went into charcter creation which I though was an improvement. Although the character creation could be better, we will get into improving that later.

For the next attempt I adjusted the initial message more. I told it to use DND 5th ed. and that it should always start with character creation. However it would only give around 5 classes to chose from. But the rest of the character creation was good. For my next run Im going to give it more info on how I want character creation to be conducted.

The next attempt I lowered the number of tokens to try and get it to run faster. I also added a message to begin immidietly with the game. When the model is run now it will get right into the character creation process without any initial prompt from the user. This uses messages.append() and it tells the model, "Are you ready to begin" and this will start the game. Also character creation now seems to have 12 classes to chose from which is an improvement. 

Overall, I think my model has improved signifigantly from where it started. It now knows it is a dungeon master and the game will begin right away. Although some things could be better with how fast it runs and with the variaty in the story it creates, I think it is a well designed model for someone who want to play a DND game and wants to use the model as the dungeon master.