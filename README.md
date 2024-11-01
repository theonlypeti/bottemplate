# Project Name

This is a template for a Discord bot project written in Python, using the nextcord library. It serves as a starting point for creating your own Discord bots.

## Template Files

The bot's functionality is divided into several template files:

- `main.py`: This is the main file that launches the bot and loads the cogs.
- `credentials\main.env`: This file contains the bot token and other sensitive information. This file is not included in the repository.
- `utils.py`: This file contains utility functions that can be used across the bot.

- `templatecog.py`: This is a general template for creating new cogs.
- `basicog.py`: This file contains basic commands and interactions for testing purposes.
- `advancedcog.py`: This file contains more advanced commands and components for the bot.
- `testing.py`: This file contains more advanced experimental test commands and interactions for the bot.
- `redditcog.py`: This is a cog that handles interactions with Reddit, including retrieving random posts from specified subreddits and sending random cat pictures.
- `wordlecog.py`: This is a template for creating a cog that implements views, buttons and a modal to implement games such as Wordle.


Each file contains example functions and commands that you can modify to suit your needs.

## Setup

1. Clone the repository.
2. Run `install.bat`
3. As per the installation instructions, supply your bot token in the `credentials\main.env` file.
4. After installation the bot should automatically launch. 

    Run the bot maunally: `python main.py`

5. Invite the bot to your server using the generated invite link from your Discord Developer Portal.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).