import yfinance as yf
from stock import Quote, Equity, Index, MultipleQuotes
import pandas as pd
import mplfinance as mpf

def get_stock_info(stock_name:str) -> dict:
    stock = yf.Ticker(stock_name)
    info = stock.info
    basic_info = stock.fast_info

    if info is None:
        return {
            'status': 'ERROR',
            'message': f'`{stock_name.upper()}`: No summary info found, symbol may be delisted.' 
        }

    try:
        quote_type = info['quoteType']
        name = info['longName'] if 'longName' in info else info['shortName']
        logo = info['logo_url']

    except Exception as e:
        return {
            'status': 'ERROR',
            'message': 'Unknown error, ticker information could not be retrieved'
            }

    try:
        price = basic_info['last_price']
        currency = basic_info['currency'] if quote_type != 'INDEX' else None
        last_close = basic_info['regular_market_previous_close']

    except Exception as e:
        return {
            'status': 'ERROR',
            'message': 'Unknown error, ticker information could not be retrieved'
            }

    return {
            'status':'OK',
            'symbol':stock_name.upper(),
            'name': name,
            'price':price, 
            'last_close':last_close,
            'currency': currency,
            'quoteType': quote_type,
            'logo': logo 
            }

def get_stock(stock_name:str) -> Quote:
    stock_info = get_stock_info(stock_name)
    if stock_info['status'] != 'OK':
        raise AssertionError(stock_info['message'])
   
    if stock_info['quoteType'] == 'INDEX':
        stock = Index(
            stock_info['symbol'], 
            stock_info['name'], 
            stock_info['price'],
            stock_info['logo']
        )
    else:
        stock = Equity(
            stock_info['symbol'],
            stock_info['name'],
            stock_info['price'], 
            stock_info['currency'],
            stock_info['logo']
        )
    return stock

def get_major_index(title:str) -> MultipleQuotes:
    sp500 = get_stock('^GSPC')
    dji = get_stock('^DJI')
    nasdaq = get_stock('^IXIC')
    ndx = get_stock('^NDX')
    return MultipleQuotes(title,[sp500, dji, nasdaq, ndx])

def get_history(stock_name:str, period:str) -> pd.DataFrame:
    if period not in ['5d','1mo','3mo','6mo','1y','2y','5y','ytd']:
        raise AssertionError('Invalid historical period.')

    stock = yf.Ticker(stock_name)
    hist = stock.history(period=period)
    return hist

def get_graph(data:pd.DataFrame, stock:Quote) -> None:
    fig, axes = mpf.plot(data,
    type='candle', 
    mav=(3), 
    volume=True,
    returnfig=True,
    ylabel=f'Price ({stock.currency})',
    style='yahoo',
    warn_too_much_data=1825)

    axes[0].set_title(stock.symbol)
    fig.savefig(fname="../media/graph.png", bbox_inches="tight")

if __name__ == "__main__":
    stock = yf.Ticker('^GSPC')
    basic_info = stock.fast_info
    print(basic_info.regular_market_previous_close)
    pass