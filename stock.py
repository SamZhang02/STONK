import discord

class Stock:

    def __init__(self, title, exchange,price):
        self.title = title
        self.exchange = exchange
        self.price = price
    
    def get_embed(self):
        embedVar = discord.Embed(title=self.title, description=self.exchange, color=0xd4f1f4)
        embedVar.add_field(name="Price", value=self.price, inline=False)
        return embedVar