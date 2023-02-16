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

logging.basicConfig(filename='info.log', encoding='utf-8', level=logging.DEBUG, format = '%(asctime)s %(levelname)-8s %(message)s')
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

    initialize(scheduler)
    logging.info(scheduler.get_jobs())

@client.event
async def on_resumed() -> None:
    print('Resumed')
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
            await message.channel.send(f"Attempted but failed to fulfill request. Error message: {e}")
            logging.error(e)

async def notify(scheduler) -> None:
    next_close = daytime.get_next_close()
    logging.info(f'Next market notification scheduled for {next_close}')

    channels = database.get_channels_to_notify()
    to_send = []
    for channel_id in channels:
        logging.info(channel_id)
        channel = client.get_channel(channel_id)
        if channel:
            to_send.append(channel)
    logging.info(to_send)

    try:
        market = get_major_index(f'Market Close - {daytime.today_date()}') 
        logging.info(market.quotes)
        for channel_to_send in to_send:
            await channel_to_send.send(embed=market.get_embed())

    except Exception as e:
        logging.error(e)
        for channel_to_send in to_send:
            await channel_to_send.send(f'Attempted but failed to send market info.')

    finally:
        scheduler.add_job(notify, 'date', args=[scheduler],run_date=next_close, misfire_grace_time=None)
        logging.info(scheduler.get_jobs())

async def wake() -> None:
    logging.info(scheduler.get_jobs())

def initialize(scheduler) -> None:
    if not os.path.exists('../database/database.db'):
        database.create_db()

    next_close = daytime.get_next_close()
    notify_is_scheduled = False 

    for job in scheduler.get_jobs():
        if job.name == 'notify':
            notify_is_scheduled = True
        if job.name == 'wake':
            scheduler.remove_job(job.id)

    scheduler.add_job(wake, 'interval', hours=1)

    if not notify_is_scheduled:
        scheduler.add_job(notify, 'date', args=[scheduler],run_date = next_close, misfire_grace_time=None)
        scheduler.start()

    logging.info(scheduler.get_jobs())
    logging.info(f'Next market notification scheduled for {next_close}')

client.run(TOKEN) # type: ignore

