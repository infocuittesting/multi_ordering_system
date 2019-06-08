from datetime import datetime
from datetime import timedelta
import pytz
def application_datetime():
    now = datetime.now()
    # assuming now contains a timezone aware datetime
    tz = pytz.timezone('Asia/Kolkata')
    yourdatetime_now = now.astimezone(tz)
    isotime  = yourdatetime_now.strftime('%Y-%m-%dT%H:%M:%SZ')
    tommorrow =yourdatetime_now+ timedelta(days=1)
    tommorrow = tommorrow.strftime('%Y-%m-%dT%H:%M:%SZ')
    #print(yourdatetime_now)
    #print("isotime:",isotime,tommorrow)
    return(isotime,tommorrow)
#application_datetime()
