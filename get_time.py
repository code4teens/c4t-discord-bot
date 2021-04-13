import pytz
from datetime import datetime
from replit import db

#takes input from datetime and returns YYYY-MM-DD
def translate_datetime(x):
    x = str(x)
    result = ''
    result = result + x[0:4] + '-'
    result = result + x[5:7] + '-'
    result = result + x[8:10]
    
    
    return result


#returns the current time in format HH:DD
def current_time():
    kct = pytz.timezone('Asia/Kuala_Lumpur')
    today = datetime.now(kct)
    today = str(today)
    return(today[11:16])

#checks which day of the camp it is
def check_day():
    today = translate_datetime(datetime.date(datetime.now()))
    for x in range(1,10):
        day = 'day' + str(x)
        if db[day] == today:
            return(day)
