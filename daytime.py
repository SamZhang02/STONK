from datetime import datetime
from pytz import timezone

def check_for_market_opening():
    today = datetime.now(timezone('EST'))
    today_date = today.weekday()
    today_time = today.time()
    if today_time.hour == 9 and today_time.minute == 30:
        return 'it is currently 9:30 AM'

