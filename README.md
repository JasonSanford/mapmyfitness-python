# mapmyfitness-python

[![Build Status](https://api.travis-ci.org/JasonSanford/mapmyfitness-python.png?branch=master)](https://travis-ci.org/JasonSanford/mapmyfitness-python)&nbsp;[![Coverage Status](https://coveralls.io/repos/JasonSanford/mapmyfitness-python/badge.png?branch=master)](https://coveralls.io/r/JasonSanford/mapmyfitness-python?branch=master)

A Python wrapper for the [MapMyFitness API](https://developer.mapmyapi.com/)

## Status

This is a work in progress:

We're tracking tasks over at [HuBoard](https://huboard.com/JasonSanford/mapmyfitness-python)

* [Routes](#routes)
* [Workouts](#workouts)
* Users*

\* not currently implemented

## Installation

Install via pip:

    pip install mapmyfitness

or from local sources:

    python setup.py install

## Dependencies

* Python 2.7, 3.2 or 3.3
* [Requests](http://docs.python-requests.org/en/latest/) takes care of our HTTP chatting, and is automatically installed when using the steps above.

## Usage

### Routes

Search for routes created by a user:

    >>> from mapmyfitness import MapMyFitness
    >>> mmf = MapMyFitness(api_key='not-so-secret', access_token='super-secret')
    >>> routes = mmf.route.search(user=9118466)  # returns a list of routes
    >>> len(routes)
    20

Get a single route:

    >>> route = mmf.route.find(348949363)
    >>> route.name
    '4 Mile Lunch Run'

Returns a RouteObject or raises `mapmyfitness.exceptions.NotFoundException` if no route is found.

Get route geometry:

    >>> route.points()
    [
        {'lat': 39.74942025, 'lng': -104.99598683, 'ele': 1604.96},
        {'lat': 39.74954872, 'lng': -104.99627271, 'ele': 1605.48},
        ...
    ]

Prefer GeoJSON?:

    >>> route.points(geojson=True)
    {
        'type': 'LineString',
        'coordinates': [
            (-104.9959868, 39.74942025),
            (-104.9961131, 39.74958007),
            ...
        ]
    }

Delete a route:

    >>> mmf.route.delete(348949363)

Returns `None` on success or raises `mapmyfitness.exceptions.NotFoundException` if the route doesn't exist.

## Validation

PEP8 validation (--ignore==E501, line length) is strictly enforced

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too:

    nosetests --with-coverage --cover-package mapmyfitness

View coverage:

    coverage html
