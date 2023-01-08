import discord
from market_info import get_stock,get_major_index,get_history, get_graph
import database
import os

async def run_command(message:discord.Message) -> None:
    content = message.content.split()
    if len(content) < 2:
        raise AssertionError("Invalid Command.")

    todo = content[1]
    match todo:
        case 'help':
            embed=discord.Embed()
            embed.set_author(name="STONK",icon_url="https://i.imgur.com/rCHzZay.jpg")
            if len(content) not in [2,3]:
                raise AssertionError("Invalid Command.")

            if len(content) == 2:
                embed.add_field(name="`help command`", value="Get help on specific commands", inline=False)
                embed.add_field(name="`get <ticker> <optional: period>`", value="Get information of a stock or an index.", inline=False)
                embed.add_field(name="`market`", value="Get current information of major indices of the US market.", inline=False)
                embed.add_field(name="`notify`", value="Enable/Disable automatic market closure info every business day in the channel where the command was sent.", inline=False)
            else:
                help_with = content[2]
                match help_with:
                    case "get":
                        embed.add_field(name="`get <ticker> <optional: period>`",value="Get information of a stock or an index.",inline=False)
                        embed.add_field(name="<ticker>", value="The stock or index's ticker.")
                        embed.add_field(name="<period>", value="""The historical period to build to graph upon.
                        - 5d: 5 days  
                        - 1mo: 1 month
                        - 3mo: 3 months
                        - 6mo: 6 months
                        - 1y: 1 year
                        - 2y: 2 years
                        - 5y: 5 years
                        - ytd: Year-to-Date
                        """,inline=False)
                    case "market":
                        embed.add_field(name="`market`", value="Get current information of major indices of the US market.", inline=False)
                    case "notify":
                        embed.add_field(name="`notify`", value="Enable/Disable automatic market closure info every business day in the channel where the command was sent.", inline=False)

            await message.channel.send(embed=embed)

        case 'hello':
            await message.channel.send('I am Ally\'s unfinished project bot.')

        case 'get':
            if len(content) not in [3,4]:
                raise AssertionError('Please use the format `stonk get <ticker>`.')
            
            ticker = content[2]

            try:
                stock = get_stock(ticker) 
                embed = stock.get_embed()
                embed.set_footer(text=f'Requested by {message.author}.',icon_url=message.author.avatar)
            except Exception as e: 
                raise AssertionError(f"{e}")

            if len(content) == 4:
                period = content[3]
                try:
                    history = get_history(ticker, period)
                    get_graph(history,stock)
                    start_date = str(history.iloc[0].name)[:10]
                    start_price = float(history.iloc[0]["Close"])
                    end_price = float(stock.price)
                    difference = end_price - start_price 
                except Exception as e: 
                    raise AssertionError(f"{e}")

                file = discord.File("../media/graph.png", filename="graph.png")
                embed.add_field(name=f'Change since {start_date}', value=f'{"%.2f" %difference} {stock.currency} ({"%.2f" %(difference/start_price * 100)}%)')
                embed.set_image(url="attachment://graph.png")
                await message.channel.send(file=file, embed=embed)
                os.remove("../media/graph.png")
            else:
                await message.channel.send(embed=embed)

        case 'market':
            try:
                indices = get_major_index('Market Right Now')
                embed = indices.get_embed()
                embed.set_footer(text=f'Requested by {message.author}.',icon_url=message.author.avatar)
                await message.channel.send(embed=embed)
            except Exception as e: 
                raise AssertionError(f"{e}")

        case 'notify':
            to_notify = database.change_notify_status(message.channel.id)
            await message.channel.send(f'Automatic market closure update in this text channel is now set to {to_notify}')

        case _:
            raise AssertionError("Invalid Command.")