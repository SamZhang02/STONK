import discord
import time
from dotenv import load_dotenv 
import os 
from pathlib import Path
from stock import Stock

#Get bot key from .env
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('I am Ally\'s unfinished project bot')
    
    if message.content.startswith == ('!stock'):
        stock = Stock('AMD','NASDAQ',69)
        await message.channel.send(embed=stock.get_embed())

client.run(TOKEN)