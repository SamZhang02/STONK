import discord

class Quote:
    def __init__(self, symbol, name,price) -> None:
        self.symbol = symbol 
        self.name = name 
        self.price = '%.2f' % price 
        self.type = 'Quote'

class Equity(Quote):
    def __init__(self, symbol, name, price, currency) -> None:
        super().__init__(symbol, name, price)
        self.currency = currency
        self.type = 'Equity'
    
    def get_embed(self) -> discord.Embed:
        embedVar = discord.Embed(title=self.symbol, description=self.name, color=0xd4f1f4)
        embedVar.add_field(name="Price", value=f'{self.price} {self.currency}', inline=False)
        return embedVar

class Index(Quote):
    def __init__(self, symbol, name, price) -> None:
        super().__init__(symbol,name,price)
        self.type = 'Index'

    def get_embed(self) -> discord.Embed:
        embedVar = discord.Embed(title=self.symbol, description=self.name, color=0xd4f1f4)
        embedVar.add_field(name="Index", value=f'{self.price} pt', inline=False)
        return embedVar