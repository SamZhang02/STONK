import pandas as pd 
import pandas_market_calendars as mcal
import datetime

def today_date() -> str:
    return str(datetime.datetime.today()).split(' ')[0]
    
def get_minutes_until_next_close() -> int:
    end = str(datetime.datetime.today() + datetime.timedelta(days=10)).split(' ')[0]
    # Create a calendar
    nyse = mcal.get_calendar('NYSE')
    interval = nyse.schedule(start_date=today_date(), end_date=end)

    current_time = pd.Timestamp(datetime.datetime.today(),tz='est')
    if current_time < mcal.date_range(interval, frequency = '1D')[0]:
        next_close = mcal.date_range(interval, frequency = '1D')[0] 
    else:
        next_close = mcal.date_range(interval, frequency = '1D')[1] 
    time_until_next_close = next_close-current_time
    return time_until_next_close.total_seconds()

if __name__ == "__main__":
    pass
