# mapmyfitness-python

[![Build Status](https://api.travis-ci.org/JasonSanford/mapmyfitness-python.png?branch=master)](https://travis-ci.org/JasonSanford/mapmyfitness-python)&nbsp;[![Coverage Status](https://coveralls.io/repos/JasonSanford/mapmyfitness-python/badge.png?branch=master)](https://coveralls.io/r/JasonSanford/mapmyfitness-python?branch=master)

A Python wrapper for the [MapMyFitness API](https://developer.mapmyapi.com/)

## Status

This is a work in progress. Current endpoints implemented are:

* [Routes](#routes)
* [Workouts](#workouts)
* [Users](#users)
* [Activity Types](#activity-types)

## Contributing

See [Contributing](CONTRIBUTING.md)

## Installation

Install via pip:

    pip install mapmyfitness

or from local sources:

    python setup.py install

## Dependencies

* Python 2.7, 3.2 or 3.3
* [Requests](http://docs.python-requests.org/en/latest/) takes care of our HTTP chatting, and is automatically installed when using the steps above.

## Usage

Instantiate an instance of `MapMyFitness` with your API key and an access token representing a user:

```python
from mapmyfitness import MapMyFitness
mmf = MapMyFitness(api_key='not-so-secret', access_token='super-secret')
```

Optionally pass `True` for `cache_finds`. This will cache instances of objects fetched through the `find` method. This is helpful for objects that aren't likely to change, like [Activity Types](#activity-type).

```python
from mapmyfitness import MapMyFitness
mmf = MapMyFitness(api_key='not-so-secret', access_token='super-secret', cache_finds=True)
```

### Routes

Implements behaviors: [find](#find), [search](#search), [create](#create), [delete](#delete), [update](#update)

#### Search Parameters

* `user` - integer - A user id to find routes for
* `users` - list or tuple - a collection of user ids to find routes for
* `close_to_location` - list or tuple - A 2-list or 2-tuple containing a latitude and longitude to search for routes near
* `minimum_distance` - int or float - The minimum distance, in meters, of routes to search for - only for use with `close_to_location`
* `maximum_distance` - int or float - The maximum distance, in meters, of routes to search for - only for use with `close_to_location`

\* One of `user`, `users` or `close_to_location` parameters must be passed.

#### Route Object Properties

* `id` - int - The unique id of the route
* `name` - str - The name of the route
* `description` - str - A description of the route
* `privacy` - str - The privacy setting of the route - one of 'Private', 'Friends' or 'Pulic'
* `distance` - float - The distance of the route in meters
* `ascent` - float - The total ascent of the route in meters
* `descent` - float - The total descent of the route in meters
* `min_elevation` - float - The minimum elevation of the route in meters
* `max_elevation` - float - The maximum elevation of the route in meters
* `city` - str - The city of the start point of the route
* `state` - str - The state of the start point of the route
* `country` - str - The country of the start point of the route
* `created_datetime` - datetime - The date and time the route was created
* `updated_datetime` - datetime - The date and time the route was updated

#### Route Object Methods

* `points()` - Returns a list of points (dicts) containing `lat`, `lng` and `ele` keys representing latitude, longitude and elevation.
* `points(geojson=True)` - Returns a [GeoJSON](http://geojson.org) LineString representation of a route.

#### Examples

Search for routes created by a user:

```python
routes_paginator = mmf.route.search(user=9118466)
```

Search for 10k routes near a specific location:

```python
routes_paginator = mmf.route.search(close_to_location=[35.555, -80.934], minimum_distance=9000, maximum_distance=11000)
```

### Workouts

Implements behaviors: [find](#find), [search](#search), [create](#create), [delete](#delete), [update](#update)

#### Search Parameters

* `user` - integer - A user id to find routes for
* `activity_type` - integer - The id of the [activity type](#activity-types) to find workouts for
* `updated_before` - datetime - A datetime to find workouts that were updated before
* `updated_after` - datetime - A datetime to find workouts that were updated after
* `created_before` - datetime - A datetime to find workouts that were created before
* `created_after` - datetime - A datetime to find workouts that were created after
* `started_before` - datetime - A datetime to find workouts that were started before
* `started_after` - datetime - A datetime to find workouts that were started after

#### Workout Object Properties

* `id` - int - The unique id of the workout
* `name` - str - The name of the route
* `privacy` - str - The privacy setting of the route - one of 'Private', 'Friends' or 'Pulic'
* `distance` - float - The distance of the route in meters
* `start_locale_timezone` - str - The timezone where the workout started
* `source` - str - The source where the workout was created
* `has_time_series` - bool - Whether the workout has time series data
* `start_datetime` - datetime - The datetime of the start of the workout
* `created_datetime` - datetime - The datetime the workout was created
* `updated_datetime` - datetime - The datetime the workout was updated
* `time_series` - list - Time series information for this workout
* `active_time_total` - int - The total active time (moving time) for the workout in seconds
* `distance_total` - int - The total distance of the workout in meters
* `steps_total` - int - The total number of steps for the workout
* `elapsed_time_total` - int - The total elapsed time (stopped and moving) for the workout
* `metabolic_energy_total` - int - The total number of calories burned for the workout
* `speed_max` - float - The max speed for the workout in meters/second
* `speed_avg` - float - The average speed for the workout in meters/second
* `route_id` - int - The id of the route of the workout if it is associated with a route
* `route` - [Route](#routes) - A route object for the route assocated with this workout, if one exists
* `activity_type_id` - int - The id of the activity type for this workout
* `activity_type` - [Activity Type](#activity-types) - An activity type object for the activity type of the workout

#### Examples

Find all workouts for a user in the year 2013

```python
start_datetime = datetime.datetime(2013, 1, 1)
end_datetime = datetime.datetime(2014, 1, 1)

workouts_paginator = mmf.workout.search(user=9118466, per_page=40, started_after=start_datetime, started_before=end_datetime)

for page_num in workouts_paginator.page_range:
    the_page = workouts_paginator.page(page_num)
    for workout in the_page:
        print(workout.start_datetime)
```

### Users

Implements behaviors: [find](#find), [search](#search)

#### Search Parameters

* `friends_with` - integer - A user id to find users that are friends with

#### User Object Properties

* `id` - int - The unique id of the user
* `first_name` - str - The first name of the user
* `last_name` - str - The last name of the user
* `username` - str - The username of the user
* `time_zone` - str - The time zone of the user
* `gender` - str - The gender of the user
* `location` - str - The location of the user
* `last_login_datetime` - datetime - The datetime of the last time the user logged in
* `join_datetime` - datetime - The datetime of the user joining MapMyFitness
* `birthdate` - date - The birthdate of the user
* `email` - str - The email address of the user
* `display_measurement_system` - str - The preferred measurement system of the user - Either 'metric' or 'imperial'
* `weight` - float - The weight of the user in kilograms
* `height` - float - The height of the user in meters

#### User Object Methods

* `get_profile_photo(size='medium')` - str - Returns a url to the profile photo of the user - Size is one of 'small', 'medium' or 'large'
* `get_friends()` - [Paginator](#paginator-properties) - A pagination object containing friends (users) of the user

### Activity Types

Implements behaviors: [find](#find)

#### Activity Type Object Properties

* `id` - int - The unique id of the activity type
* `name` - str - The name of the activity type
* `has_parent` - bool - Whether the activity type has a parent activity type
* `root_activity_type_id` - int - The unique id of the root activity type of this activity type
* `root_activity_type` - [Activity Type](#activity-types) - The root activity type of this activity type

## Behaviors

### find

Find a single object by its unique id. Returns a object or raises `mapmyfitness.exceptions.NotFoundException` if no object is found.

#### Example

```python
route = mmf.route.find(348949363)
print(route.name)  # '4 Mile Lunch Run'
```

### search

Search for objects. Returns a [Paginator object](https://github.com/JasonSanford/mapmyfitness-python/blob/master/mapmyfitness/paginator.py#L8) to easily page through large result sets.

See [this gist](https://gist.github.com/JasonSanford/ddbe06832e5d17061b8a) for implementation details.

#### Paginator Properties

* `count` - returns the total number of objects on all pages.
* `num_pages` - returns the number of pagees in the paginator.
* `page_range` - returns a range of page numbers to allow for iteration of pages.

#### Paginator Methods

* `page(<page_number>)` - returns a [Page object](https://github.com/JasonSanford/mapmyfitness-python/blob/master/mapmyfitness/paginator.py#L63) containing objects on a specific page.

#### Example Usage

```python
start_datetime = datetime.datetime(2014, 1, 1)
end_datetime = datetime.datetime(2015, 1, 1)

workouts_paginator = mmf.workout.search(user=9118466, per_page=40, started_after=start_datetime, started_before=end_datetime)

page_count = workouts_paginator.num_pages  # 2
page_range = workouts_paginator.page_range # [1, 2]
total_count = workouts_paginator.count # 58

for page_num in page_range:
    the_page = workouts_paginator.page(page_num)
    print(the_page)  # <Page 1 of 2>
    for workout in the_page:
        print(workout.start_datetime)  # 2014-01-02 02:59:53+00:00
```

### create

Create an object.

### delete

Delete an object.

#### Example

```python
mmf.route.delete(348949363)
```

Returns `None` on success or raises `mapmyfitness.exceptions.NotFoundException` if the object doesn't exist.

### update

Update an object.
