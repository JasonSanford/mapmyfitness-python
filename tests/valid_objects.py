import datetime

from mapmyfitness.constants import PRIVATE, BIKE_RIDE


route = {
    'name': 'My Commute',
    'description': 'This is a super-simplified route of my commute.',
    'city': 'Littleton',
    'country': 'US',
    'distance': 25749.5,
    'privacy': PRIVATE,
    'state': 'CO',
    'points': [
        {'lat': 39.5735, 'lng': -105.0164},
        {'lat': 39.6781, 'lng': -104.9926},
        {'lat': 39.75009, 'lng': -104.99656}
    ]
}

workout = workout = {
    'user': 14122640,
    'name': 'Test workout via API',
    'start_datetime': datetime.datetime(2014, 1, 9, 10, 8, 7),
    'activity_type': BIKE_RIDE,
    'active_time_total': 600,
    'elapsed_time_total': 650,
}
