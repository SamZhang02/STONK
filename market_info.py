import yfinance as yf
from stock import Quote, Equity, Index, MultipleQuotes

def get_stock_info(stock_name:str) -> dict:
    stock = yf.Ticker(stock_name)
    info = stock.info

    if info is None:
        return {
            'status': 'ERROR',
            'message': f'`{stock_name.upper()}`: No summary info found, symbol may be delisted.' 
        }

    try:
        symbol = info['symbol']
        quote_type = info['quoteType']
        name = info['longName'] if 'longName' in info else info['shortName']
        price = info['regularMarketPrice']
        currency = info['currency'] if quote_type != 'INDEX' else None
        logo = info['logo_url']

        return {
            'status':'OK',
            'symbol':symbol,
            'name' :name,
            'price': price,
            'currency': currency,
            'quoteType': quote_type,
            'logo': logo
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

if __name__ == "__main__":
    print(get_stock_info('erwer'))
    pass
