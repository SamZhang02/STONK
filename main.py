import discord
from discord.ext import tasks 
import os 
from pathlib import Path
from dotenv import load_dotenv 
from commands import run_command
import database
from daytime import get_minutes_until_next_close,today_date
from market_info import get_major_index


#Get bot key from .env
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready() -> None:
    print(f'Logged in as {client.user}')
    notify.start()

@client.event
async def on_message(message:discord.Message) -> None:
    if message.author == client.user:
        return
    
    if message.content.startswith('stonk'):
        try:
            await run_command(message)
            await message.add_reaction('✅')
        except Exception as e:
            await message.add_reaction('❌')
            await message.channel.send(e)

@tasks.loop(seconds=get_minutes_until_next_close())
async def notify() -> None:
    channels = database.get_channels_to_notify()
    market = get_major_index(f'Market Close - {today_date()}')
    for channel_id in channels:
        channel = client.get_channel(channel_id)
        try:
            await channel.send(embed=market.get_embed())
        except:
            pass
    notify.change_interval(seconds=get_minutes_until_next_close())

client.run(TOKEN) # type: ignore
