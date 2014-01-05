mapmyfitness-python
===================



# mapmyfitness-python

[![Build Status](https://api.travis-ci.org/JasonSanford/mapmyfitness-python.png)](https://travis-ci.org/JasonSanford/mapmyfitness-python)&nbsp;[![Coverage Status](https://coveralls.io/repos/JasonSanford/mapmyfitness-python/badge.png?branch=master)](https://coveralls.io/r/JasonSanford/mapmyfitness-python?branch=master)

A Python wrapper for the [MapMyFitness API](https://developer.mapmyapi.com/)

## Status

This is a work in progress:

* [Routes](#routes)
* Workouts*

\* not currently implemented

## Installation

Install via pip:

    pip install mapmyfitness

or from local sources:

    python setup.py install

## Dependencies

Just one - [Requests](http://docs.python-requests.org/en/latest/) takes care of our HTTP chatting, and is automatically installed when using the steps above.

## Usage

    # TODO: this

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too:

    nosetests --with-coverage --cover-package mapmyfitness

View coverage:

    coverage html
