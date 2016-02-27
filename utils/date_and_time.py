from pytz import timezone, country_timezones, utc
import datetime


def get_date_and_time_with_timezone(country='UA', date=True, time=False):
    country = timezone(country_timezones[country][0])
    date_time_str = ''
    if date:
        date_time_str += '%Y-%m-%d'
    if time:
        date_time_str += ' %H:%M:%S'
    date = utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(
        country).strftime(date_time_str)
    return date


def hours_minutes_seconds_from_seconds(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    seconds = seconds % 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)
