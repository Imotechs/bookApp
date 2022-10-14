import datetime

def get_date_due():
    now = datetime.datetime.now()
    nday = datetime.timedelta(days = 10)
    due_time = now + nday
    return now, due_time

