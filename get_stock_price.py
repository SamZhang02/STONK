import yfinance as yf

def get_stock_info(stock_name:str) -> dict:
    stock = yf.Ticker(stock_name)
    info = stock.info
    if info['regularMarketPrice'] is None:
        return {
            'status': 'ERROR',
            'message': 'Stock ticker does not exist.' 
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

    except:
        return {
            'status': 'ERROR',
            'message': 'Unknown error, stock information could not be retrieved'
            }


if __name__ == "__main__":
    pass