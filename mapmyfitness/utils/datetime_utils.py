import datetime

from mapmyfitness.timezones import utc


def iso_format_to_datetime(iso_format):
    relevant_str = iso_format.split('+')[0]
    date, time = relevant_str.split('T')
    year, month, day = map(int, date.split('-'))
    hour, minute, second = map(int, time.split(':'))
    return datetime.datetime(year, month, day, hour, minute, second, tzinfo=utc)
