# ClimaCell-Python

A python interface to the [Climacell Weather
API](https://www.climacell.co/weather-api/)

## Installation

Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a
package manager for Python.

    pip install climacell-python

This library supports the following Python implementations:

* Python 3.5
* Python 3.6
* Python 3.7
* Python 3.8

## Getting Started

Getting started with the ClimaCell API is easy. Create a
`ClimacellApiClient` and you ready to start making requests.

### API Credentials

The `ClimacellApiClient` needs your Climacell key found in your dashboard. Pass this directly to the constructor

```python
from climacell_api.client import ClimacellApiClient

key = "XXXXXXXXXXXXXXXXX"
client = ClimacellApiClient(key)
```

### ClimaCell Documentation

Checkout the [ClimaCell docs](https://developer.climacell.co/) for details on their Weather API.

The fields parameter is important for selecting the data you want to retrieve. A list of all possible fields and which endpoint accepts them can be found [here](https://developer.climacell.co/v3/reference#data-layers-weather).

## Making Requests


The client will return a ClimacellResponse object which is a wrapper around [requests](https://pypi.org/project/requests/)' response object.

You can call all the normal requests' response methods plus a data() method with all the ClimaCell specific data.

The measurements property on data is a dictionary providing the field results using the field strings as keys. A list of all fields accepted per endpoint can be found [here](https://developer.climacell.co/v3/reference#data-layers-weather).


Below are examples for all the endpoints this library supports.


### Realtime

Data returned is single up to the minute observation for a specific location.

```python
>>> from climacell_api import ClimacellApiClient
>>> client = ClimacellApiClient(YOUR_KEY)
>>> r = client.realtime(lat=40, lon=50, fields=['temp', 'wind_gust'])
>>> r.status_code
200
>>> r.json() # for raw json
{ 'lat': 40, 'lon': 50, ...}
>>> data = r.data()
>>> data.lat
40
>>> data.lon
50
>>> data.observation_time
datetime.datetime(2020, 6, 26, 13, 45, 26, tzinfo=tzutc())
>>> measurements = data.measurements
>>> measurements['temp'].value
43
>>> measurements['temp'].units
'C'
>>> measurements['wind_gust'].value
7.5
>>> measurements['wind_gust'].units
'm/s'
```

### Nowcast

Data returned is a list of forecast data for a specific location.

```python
>>> from climacell_api import ClimacellApiClient
>>> client = ClimacellApiClient(YOUR_KEY)
>>> r = client.nowcast(lat=40, lon=50, timestep=30, start_time='now', end_time='2020-06-22T20:47:00Z' fields=['temp', 'wind_gust'])
>>> r.status_code
200
>>> r.json() # for raw json
[{ 'lat': 40, 'lon': 50, ...}, { 'lat': 40, 'lon': 50, ...}, ...]
>>> data = r.data()
>>> data[0].lat
40
>>> data[0].lon
50
>>> data[0].observation_time
datetime.datetime(2020, 6, 26, 13, 45, 26, tzinfo=tzutc())
>>> measurements = data[0].measurements
>>> measurements['temp'].value
43
>>> measurements['temp'].units
'C'
>>> measurements['wind_gust'].value
7.5
>>> measurements['wind_gust'].units
'm/s'
```

### Hourly Forecast

Data returned is a list of forecast data for a specific location up 96 hours in the future.

```python
>>> from climacell_api import ClimacellApiClient
>>> client = ClimacellApiClient(YOUR_KEY)
>>> r = client.forecast_hourly(lat=40, lon=50, start_time='now', end_time='2020-06-22T20:47:00Z' fields=['temp', 'wind_gust'])
>>> r.status_code
200
>>> r.json() # for raw json
[{ 'lat': 40, 'lon': 50, ...}, { 'lat': 40, 'lon': 50, ...}, ...]
>>> data = r.data()
>>> data[0].lat
40
>>> data[0].lon
50
>>> data[0].observation_time
datetime.datetime(2020, 6, 26, 13, 45, 26, tzinfo=tzutc())
>>> measurements = data[0].measurements
>>> measurements['temp'].value
43
>>> measurements['temp'].units
'C'
>>> measurements['wind_gust'].value
7.5
>>> measurements['wind_gust'].units
'm/s'
```

### Daily Forecast

Data returned is a list of daily forecast data for a specific location up to 15 days in the future. Daily forecast data has max and min data for many fields. For example the temp max would high temp for the day and temp min would be the low temp for the day. Included with this is the forecasted observation time of the min and max data points.

```python
>>> from climacell_api import ClimacellApiClient
>>> client = ClimacellApiClient(YOUR_KEY)
>>> r = client.forecast_daily(lat=40, lon=50, start_time='now', end_time='2020-06-22T20:47:00Z' fields=['temp'])
>>> r.status_code
200
>>> r.json() # for raw json
[{ 'lat': 40, 'lon': 50, ...}, { 'lat': 40, 'lon': 50, ...}, ...]
>>> data = r.data()
>>> data[0].lat
40
>>> data[0].lon
50
>>> data[0].observation_time
datetime.datetime(2020, 6, 26)
>>> measurements = data[0].measurements
>>> measurements['temp']['max'].value
43
>>> measurements['temp']['max'].units
'C'
>>> measurements['temp']['max'].observation_time
datetime.datetime(2020, 6, 26, 13, 45, 26, tzinfo=tzutc())
>>> measurements = data[0].measurements
>>> measurements['temp']['min'].value
31
>>> measurements['temp']['min'].units
'C'
>>> measurements['temp']['min'].observation_time
datetime.datetime(2020, 6, 26, 23, 45, 26, tzinfo=tzutc())
```
### Historical ClimaCell

Data returned is a list of forecast data for a specific location up to 6 hours in the past.

```python
>>> from climacell_api import ClimacellApiClient
>>> client = ClimacellApiClient(YOUR_KEY)
>>> r = client.historical_climacell(lat=40, lon=50, timestep=30, start_time='2020-06-22T20:47:00Z', end_time='now' fields=['temp', 'wind_gust'])
>>> r.status_code
200
>>> r.json() # for raw json
[{ 'lat': 40, 'lon': 50, ...}, { 'lat': 40, 'lon': 50, ...}, ...]
>>> data = r.data()
>>> data[0].lat
40
>>> data[0].lon
50
>>> data[0].observation_time
datetime.datetime(2020, 6, 26, 13, 45, 26, tzinfo=tzutc())
>>> measurements = data[0].measurements
>>> measurements['temp'].value
43
>>> measurements['temp'].units
'C'
>>> measurements['wind_gust'].value
7.5
>>> measurements['wind_gust'].units
'm/s'
```

### Historical Station

Data returned is a list of forecast data for a specific location up to 4 weeks in the past. This is data from weather stations and not climacell specific readings

```python
>>> from climacell_api import ClimacellApiClient
>>> client = ClimacellApiClient(YOUR_KEY)
>>> r = client.historical_station(lat=40, lon=50, start_time='2020-06-22T20:47:00Z', end_time='now' fields=['temp', 'wind_gust'])
>>> r.status_code
200
>>> r.json() # for raw json
[{ 'lat': 40, 'lon': 50, ...}, { 'lat': 40, 'lon': 50, ...}, ...]
>>> data = r.data()
>>> data[0].lat
40
>>> data[0].lon
50
>>> data[0].observation_time
datetime.datetime(2020, 6, 26, 13, 45, 26, tzinfo=tzutc())
>>> measurements = data[0].measurements
>>> measurements['temp'].value
43
>>> measurements['temp'].units
'C'
>>> measurements['wind_gust'].value
7.5
>>> measurements['wind_gust'].units
'm/s'
```

### Insights Fire Index

Data returned is a single fire index based on 20 year average for the location

```python
>>> from climacell_api import ClimacellApiClient
>>> client = ClimacellApiClient(YOUR_KEY)
>>> r = client.insights_fire_index(lat=40, lon=50)
>>> r.status_code
200
>>> r.json() # for raw json
[{ 'fire_index': 22.123 }]
>>> data = r.data()
>>> data.fire_index
22.123
```

### Errors
Error messages are handled by returning the code and message from the data() method

```python
>>> from climacell_api import ClimacellApiClient
>>> client = ClimacellApiClient(YOUR_KEY)
>>> r = client.realtime(lat=40, lon=9999, fields=['temp'])
>>> r.status_code
400
>>> r.json() # for raw json
{'statusCode': 400, 'errorCode': 'BadRequest', 'message': 'lon must be in the range -180..180'}
>>> data = r.data()
>>> data.error_code
'BadRequest'
>>> data.error_message
'lon must be in the range -180..180'
```



### Units

Each endpoint, except for fire_index, takes an optional units parameter.

```python
units='si' # Default value and returns the scientific unit of measurement for the field

units='us' # Returns the US unit of measurement for the field.
```

## Contributing

### Submitting a Pull Request

1. [Fork](https://help.github.com/articles/fork-a-repo/) the [official repository](https://github.com/nicolo/climacell-python).
2. [Create a topic branch.](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/)
3. Implement your feature or bug fix.
4. Add, commit, and push your changes.
5. [Submit a pull request.](https://help.github.com/articles/using-pull-requests/)

### Running the Test Suite

```console
$ pip install -e .[dev]

$ pytest
```
