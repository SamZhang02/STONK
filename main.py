import discord
from dotenv import load_dotenv 
import os 
from pathlib import Path
from stock import Equity, Index 
from get_stock_price import get_stock_info

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
        
        stock_info = get_stock_info(ticker)
        if stock_info['status'] != 'OK':
            await message.channel.send(stock_info['message'])
            return
        
        if stock_info['quoteType'] == 'INDEX':
            stock = Index(stock_info['symbol'], stock_info['name'], stock_info['price'])
        else:
            stock = Equity(stock_info['symbol'], stock_info['name'], stock_info['price'], stock_info['currency'])

        await message.channel.send(embed=stock.get_embed())

client.run(TOKEN)