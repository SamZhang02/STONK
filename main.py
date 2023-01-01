import logging
import os
from pathlib import Path

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

import database
import daytime
from commands import run_command
from market_info import get_major_index

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Logging starts here')

#Get bot key from .env
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler(timezone='America/Toronto')

@client.event
async def on_ready() -> None:
    print(f'Logged in as {client.user}')
    logging.info(f'Logged in as {client.user}')
    if not os.path.exists('database.db'):
        database.create_db()

    # TODO: Check if there is currently a scheduler -> check if there are any expired jobs in scheduled jobs 

    next_close = daytime.get_next_close()

    notify_is_scheduled = False 
    surprise_is_scheduled = False

    for job in scheduler.get_jobs():
        if job.name == 'notify':
            notify_is_scheduled = True
        if job.name == 'surprise':
            surprise_is_scheduled = True

    if not notify_is_scheduled:
        scheduler.add_job(notify, 'date', args=[scheduler],run_date = next_close)
    if not surprise_is_scheduled:
        scheduler.add_job(surprise, 'date', run_date = daytime.new_year())
    scheduler.start()
    
    scheduler.print_jobs()
    print(f'Next market notification scheduled for {next_close}')
    logging.info(f'Next market notification scheduled for {next_close}')

@client.event
async def on_resumed() -> None:
    logging.info(f'Resumed')

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

async def notify(scheduler) -> None:
    channels = database.get_channels_to_notify()
    logging.info(channels)
    market = get_major_index(f'Market Close - {daytime.today_date()}') 
    logging.info(market.quotes)
    for channel_id in channels:
        channel = client.get_channel(channel_id)
        try:
            await channel.send(embed=market.get_embed())
        except Exception as e:
            logging.error(e)

    next_close = daytime.get_next_close()
    scheduler.add_job(notify, 'date', args=[scheduler],run_date = next_close)

    scheduler.print_jobs()
    print(f'Next market notification scheduled for {next_close}')
    logging.info(f'Next market notification scheduled for {next_close}')
    
async def surprise() -> None:
    channels = [1038924910287917068,927282187424899072]
    for x in channels:
        channel = client.get_channel(x)
        await channel.send("Hello, this is a scheduled message from Sam:\nHappy New Year.\n(If this did not send at midnight then Sam is dumb and can't code)")



client.run(TOKEN) # type: ignore
