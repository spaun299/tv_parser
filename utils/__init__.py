import datetime
import pytz


def get_current_datetime(timezone='Europe/Moscow'):
    dt = datetime.datetime.now(pytz.timezone(timezone))
    return datetime.datetime(dt.year, dt.month, dt.day, hour=dt.hour, minute=dt.minute)