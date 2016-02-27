from pytz import timezone, country_timezones
import datetime


def get_date_time(country='UA'):
    country = timezone(country_timezones[country][0])
    date = country.localize(datetime.datetime.today()).strftime('%Y-%m-%d')
    return date


def hours_minutes_seconds_from_seconds(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    seconds = seconds % 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)
