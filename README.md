[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/sgLta_qa)
# Virtual assistant
A portal from discord to LLM functionality with some additional features

## Usage
The bot cannot simply be invited, it has to be hosted locally. Hence, To use the bot you have to:

1. Create a application through the discord developer enviorment https://discord.com/developers/applications.
2. Make it a bot and make it request message reading and sending privlages.
3. Invite the bot to the server on which you want to have access to it.
4. Save the appliation's token

The bot also requires a valid openai Token. To get one:
1. Access https://platform.openai.com/docs/api-reference
2. Create an account
3. Set up billing
4. View api-keys, copy key

Then, to run the bot
1. Paste the key and token into your .env file.
2. *name of assitant*="*Your discord token", *OPENAI_KEY*="*Your openai token*"
    The name of the assistant must match one avalible options from the assistant.py file.
    More on that later.
3. Run the file and select assistant by inputting the associated index

The projects allows you to create custom assitant personalities. To do this:
1. Open the assistants.py file
2. Create a assistant object.
    *name of assistant* = Assistant("*Personality description*")
3. Add the assistant object to the list_of_available_assistants
4. Save everything

## Requirements
* openai module and key
* discord module
* dotenv
