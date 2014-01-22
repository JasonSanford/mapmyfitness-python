import datetime

from .timezones import utc


def privacy_enum_to_string(privacy_enum):
    #
    # From constants:
    # PRIVATE = 0
    # PUBLIC = 3
    # FRIENDS = 1
    #
    privacy_map = {
        0: 'Private',
        1: 'Friends',
        3: 'Public'
    }
    return privacy_map[privacy_enum]


def iso_format_to_datetime(iso_format):
    relevant_str = iso_format.split('+')[0]
    date, time = relevant_str.split('T')
    year, month, day = map(int, date.split('-'))
    hour, minute, second = map(float, time.split(':'))
    hour, minute, second = map(int, (hour, minute, second))
    return datetime.datetime(year, month, day, hour, minute, second, tzinfo=utc)


def datetime_to_iso_format(dt):
    utc_datetime = dt.replace(tzinfo=utc)
    return utc_datetime.isoformat()
