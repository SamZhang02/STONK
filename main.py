import discord
from dotenv import load_dotenv 
import os 
from pathlib import Path
import asyncio
from commands import run_command


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
    
    if message.content.startswith('stonk'):
        try:
            await run_command(message)
        except Exception as e: 
            await message.channel.send(f'Error: {e}')
            

    if message.content.startswith('!market'):
        indices = get_major_index('Market Right Now')
        await message.channel.send(embed=indices.get_embed())

client.run(TOKEN)