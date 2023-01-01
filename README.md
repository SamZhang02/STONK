# STONK

[![discord.py Library](https://img.shields.io/badge/discord.py-2.1.0-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python 3](https://img.shields.io/badge/python-3.10.9-blue.svg)](https://www.python.org/)

Discord bot that allows for the retrieval of the stock market's information via user commands.

## REQUIREMENTS

Libraries: `pip install -r requirements.txt`

Database: SQLite3

### To create you own instance:

`.env` file with a Discord bot API key from the Discord Developper Portal to create your own discord bot instance.

### To invite my instance of the bot to your server:

Link: https://discord.com/oauth2/authorize?client_id=1048012729711087626&permissions=274877930560&scope=bot

The bot is not currently being hosted anywhere yet, but will be very soon. 

## ROADMAP
- Implement price change since open in all commands
- Implement embeds' color change depending of whether change since open is positive or negative

## COMMANDS
All commands start with the prefix `stonk` (Caps sensitive) 

`stonk help`

Retrieve all possible bot commands.

<p align="center">
  <img src="https://user-images.githubusercontent.com/112342947/209816158-cea4084c-4f61-4f24-bcc4-4f82b1ca8116.png">
</p>

`stonk get <ticker>`

Retrieve information on a single stock ticker (All markets)

<p align="center">
  <img src="https://user-images.githubusercontent.com/112342947/210170963-3b2783ef-bbd2-4ddc-9dee-eab7c936ad03.png">
</p>

`stonk market`

Retrieve information on major indices of the U.S. stock market

<p align="center">
  <img src="https://user-images.githubusercontent.com/112342947/209816402-24b6e059-c736-4634-9202-9a06ef65bdab.png">
</p>

`stonk notify`

Enable/disable daily automatic market update on major indices of the U.S. stock market in a specific chatroom
<p align="center">
  <img src="https://user-images.githubusercontent.com/112342947/209816417-912bdbe5-b2fa-4734-9c74-7e96ee9eec89.png">
</p>

