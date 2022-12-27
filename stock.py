import discord

class Quote:
    def __init__(self, symbol:str, name:str, price:int) -> None:
        self.symbol = symbol 
        self.name = name 
        self.price = '%.2f' % price 

class Equity(Quote):
    def __init__(self, symbol:str, name:str, price:int, currency:str) -> None:
        super().__init__(symbol, name, price)
        self.currency = currency
    
    def get_embed(self) -> discord.Embed:
        embedVar = discord.Embed(title=self.name, description=self.symbol, color=0xd4f1f4)
        embedVar.add_field(name="Price", value=f'{self.price} {self.currency}', inline=False)
        return embedVar

class Index(Quote):
    def __init__(self, symbol:str, name:str, price:int) -> None:
        super().__init__(symbol,name,price)
        self.currency = 'px' 

    def get_embed(self) -> discord.Embed:
        embedVar = discord.Embed(title=self.name, description=self.symbol, color=0xd4f1f4)
        embedVar.add_field(name="Index", value=f'{self.price} {self.currency}', inline=False)
        return embedVar
    
class MultipleQuotes:
    def __init__(self, title, quotes:list) -> None:
        self.quotes = quotes
        self.title = title

    def get_embed(self) -> discord.Embed:
        embedVar = discord.Embed(title= self.title, color=0xd4f1f4)
        for index in self.quotes:
            embedVar.add_field(name=index.name, value=f'{index.price} {index.currency}', inline=False)
        return embedVar