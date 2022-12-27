import discord
from market_info import get_stock,get_major_index
import database

async def run_command(message:discord.Message) -> None:
    content = message.content.split()
    if len(content) < 2:
        raise AssertionError("Invalid Command.")

    todo = content[1]
    if todo == 'help':
        embed=discord.Embed()
        embed.set_author(name="STONK", icon_url="https://i.imgur.com/rCHzZay.jpg")
        embed.add_field(name="get <ticker>", value="Get current information of a stock or an index.", inline=False)
        embed.add_field(name="market", value="Get current information of major indices of the US market.", inline=False)
        embed.add_field(name="notify", value="Enable/Disable automatic market closure info every business day in the channel where the command was sent.", inline=False)

        await message.channel.send(embed=embed)

    elif todo == 'hello':
        await message.channel.send('I am Ally\'s unfinished project bot.')

    elif todo == 'get':
        if len(content) != 3:
            raise AssertionError('Please use the format stonk get <ticker>.')
        
        ticker = content[2]

        try:
            stock = get_stock(ticker) 
            await message.channel.send(embed=stock.get_embed())
        except Exception as e: 
            raise AssertionError(f"{e}")

    elif todo == 'market':
        try:
            indices = get_major_index('Market Right Now')
            await message.channel.send(embed=indices.get_embed())
        except Exception as e: 
            raise AssertionError(f"{e}")

    elif todo == 'notify':
        to_notify = database.change_notify_status(message.channel.id)
        await message.channel.send(f'Automatic market closure update in this text channel is now set to {to_notify}')

    else:
        raise AssertionError("Invalid Command.")