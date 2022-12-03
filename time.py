from datetime import datetime
from pytz import timezone

tz = timezone('EST')
today = datetime.now(tz)
today_date = today.weekday()
today_time = today.time()
print(today_time)

