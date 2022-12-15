import discord
from dotenv import load_dotenv 
import os 
from pathlib import Path
from stock import Equity, Index, MultipleQuotes
from market_info import get_stock,get_major_index

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
    
    #TODO: put commands in another module
    # if message.content.startswith('!'):
    #     run_command()

    if message.content.startswith('!hello'):
        await message.channel.send('I am Ally\'s unfinished project bot')
    
    if message.content.startswith('!stonk'):
        content = message.content.split()
        if len(content) != 2:
            await message.channel.send('Invalid Command.')
            return
        ticker = content[1]
        
        try:
            stock = get_stock(ticker) 
        except Exception as e: 
            await message.channel.send(str(e))
            return

        if type(stock) == str:
            await message.channel.send(stock)
            return
            
        await message.channel.send(embed=stock.get_embed())

    if message.content.startswith('!market'):
        indices = get_major_index('Market Right Now')
        await message.channel.send(embed=indices.get_embed())

client.run(TOKEN)