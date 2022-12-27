import yfinance as yf
from stock import Quote, Equity, Index, MultipleQuotes

def get_stock_info(stock_name:str) -> dict:
    stock = yf.Ticker(stock_name)
    info = stock.info
    if info['regularMarketPrice'] is None:
        return {
            'status': 'ERROR',
            'message': 'There is no currently available price for one or more tickers requested.' 
        }

    try:
        symbol = info['symbol']
        quote_type = info['quoteType']
        name = info['longName'] if 'longName' in info else info['shortName']
        price = info['regularMarketPrice']
        currency = info['currency'] if quote_type != 'INDEX' else None

        return {
            'status':'OK',
            'symbol':symbol,
            'name' :name,
            'price': price,
            'currency': currency,
            'quoteType': quote_type
        }

    except Exception as e:
        return {
            'status': 'ERROR',
            'message': 'Unknown error, ticker information could not be retrieved'
            }

def get_stock(stock_name:str) -> Quote:
    stock_info = get_stock_info(stock_name)
    if stock_info['status'] != 'OK':
        raise AssertionError(stock_info['message'])
   
    if stock_info['quoteType'] == 'INDEX':
        stock = Index(
            stock_info['symbol'], 
            stock_info['name'], 
            stock_info['price']
        )
    else:
        stock = Equity(
            stock_info['symbol'],
            stock_info['name'],
            stock_info['price'], 
            stock_info['currency']
        )
    return stock

def get_major_index(title:str) -> MultipleQuotes:
    sp500 = get_stock('^GSPC')
    dji = get_stock('^DJI')
    nasdaq = get_stock('^IXIC')
    ndx = get_stock('^NDX')
    return MultipleQuotes(title,[sp500, dji, nasdaq, ndx])

if __name__ == "__main__":
    pass