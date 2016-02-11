from pytz import timezone, country_timezones
import datetime


def get_date_time(country='UA'):
    country = timezone(country_timezones[country][0])
    date = country.localize(datetime.datetime.today()).strftime('%Y-%m-%d')
    return date
