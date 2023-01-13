# STONK
UPDATE Jan 13 2023: The bot is currently [broken](https://github.com/SamZhang02/STONK/issues/1), for specifics, please view the linked issue. 

[![discord.py Library](https://img.shields.io/badge/discord.py-2.1.0-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python 3](https://img.shields.io/badge/python-3.10.9-blue.svg)](https://www.python.org/)

Discord bot that allows for the retrieval of the stock market's information via user commands.

## REQUIREMENTS

Libraries: `pip install -r requirements.txt`

Database: SQLite3

### To create you own instance:

`.env` file with a Discord bot API key from the Discord Developper Portal to create your own discord bot instance.

### To invite my instance of the bot to your server:

Link: https://discordapp.com/oauth2/authorize?&client_id=1048012729711087626&scope=bot

## ROADMAP
- Implement price change since open in all commands
- Implement embeds' color change depending of whether change since open is positive or negative

## COMMANDS
All commands start with the prefix `stonk` (Caps sensitive) 

`stonk help` to retrieve all possible bot commands

Retrieve all possible bot commands.

<p align="center">
<img src=https://user-images.githubusercontent.com/112342947/211911255-c7081ddd-8bab-4a61-aba7-6ee8432573a6.png>

</p>

## CREDITS
The underlying API wrapper for the discord bot is [discord.py](https://github.com/Rapptz/discord.py).

Most of the stock market's information are retrieved using the [yfinance](https://github.com/ranaroussi/yfinance) library. 
