from datetime import datetime, timedelta, timezone
import dateutil.parser
import os
import vcr
from climacell_api.client import ClimacellApiClient

my_vcr = vcr.VCR(filter_query_parameters=[('apikey', 'CLIMACELL_API_KEY')])


@my_vcr.use_cassette('tests/vcr_cassettes/realtime-lat12-lon13.yml')
def test_real_time():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    response = api_client.realtime(
            lat='12', lon='13', units='us', fields=['wind_gust', 'temp'])

    assert response.status_code == 200
    data = response.data()
    assert data.lat == 12
    assert data.lon == 13
    assert data.observation_time == dateutil.parser.parse(
            '2020-06-22T20:44:29.185Z')
    measurements = data.measurements
    assert measurements['temp'].value == 96.46
    assert measurements['temp'].units == 'F'
    assert measurements['wind_gust'].value == 10.07
    assert measurements['wind_gust'].units == 'mph'
    assert response.json() == {
            'lat': 12,
            'lon': 13,
            'observation_time': {'value': '2020-06-22T20:44:29.185Z'},
            'temp': {'units': 'F', 'value': 96.46},
            'wind_gust': {'units': 'mph', 'value': 10.07}
            }


@my_vcr.use_cassette('tests/vcr_cassettes/realtime-bad-lon.yml')
def test_bad_params():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    response = api_client.realtime(
            lat='12', lon='999', fields=['wind_gust'])

    assert response.status_code == 400
    data = response.data()
    assert data.error_code == 'BadRequest'
    assert data.error_message == 'lon must be in the range -180..180'
    assert response.json() == {
            'statusCode': 400,
            'errorCode': 'BadRequest',
            'message': 'lon must be in the range -180..180',
            }


@my_vcr.use_cassette('tests/vcr_cassettes/nowcast-no-end-time.yml')
def test_nowcast():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    response = api_client.nowcast(
            lat='40', lon='80', timestep=30, start_time='now', units='us',
            fields=['wind_gust', 'precipitation_type'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 13
    assert data[0].lat == 40
    assert data[0].lon == 80
    assert data[0].observation_time == dateutil.parser.parse(
            '2020-06-22T20:47:00.196Z')
    measurements = data[0].measurements
    assert measurements['precipitation_type'].value == 'none'
    assert measurements['precipitation_type'].units is None
    assert measurements['wind_gust'].value == 13.42
    assert measurements['wind_gust'].units == 'mph'
    assert response.json()[0] == {
            'lat': 40,
            'lon': 80,
            'observation_time': {'value': '2020-06-22T20:47:00.196Z'},
            'wind_gust': {'units': 'mph', 'value': 13.42},
            'precipitation_type': {'value': 'none'}
            }


@my_vcr.use_cassette('tests/vcr_cassettes/nowcast-with-end-time.yml')
def test_nowcast_with_end_time():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    start_time = datetime(2020, 6, 22, 23, tzinfo=timezone.utc)
    end_time = start_time + timedelta(minutes=60)
    response = api_client.nowcast(
            lat='40', lon='80', timestep=30,
            start_time=start_time.isoformat(), end_time=end_time.isoformat(),
            fields=['wind_gust', 'precipitation_type'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 3
    assert data[0].lat == 40
    assert data[0].lon == 80
    assert data[0].observation_time == dateutil.parser.parse(
            '2020-06-22T23:00:00.000Z')
    measurements = data[0].measurements
    assert measurements['precipitation_type'].value == 'none'
    assert measurements['precipitation_type'].units is None
    assert measurements['wind_gust'].value == 3
    assert measurements['wind_gust'].units == 'm/s'
    assert response.json()[0] == {
            'lat': 40,
            'lon': 80,
            'observation_time': {'value': '2020-06-22T23:00:00.000Z'},
            'wind_gust': {'units': 'm/s', 'value': 3},
            'precipitation_type': {'value': 'none'}
            }


@my_vcr.use_cassette('tests/vcr_cassettes/forecast-hourly-no-end-time.yml')
def test_forecast_hourly():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    response = api_client.forecast_hourly(
            lat='43.08', lon='-89.54', start_time='now',
            fields=['wind_gust', 'precipitation_type'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 109
    assert data[0].lat == 43.08
    assert data[0].lon == -89.54
    assert data[0].observation_time == dateutil.parser.parse(
            '2020-06-22T20:00:00.000Z')
    measurements = data[0].measurements
    assert measurements['precipitation_type'].value == 'rain'
    assert measurements['precipitation_type'].units is None
    assert measurements['wind_gust'].value == 3.49
    assert measurements['wind_gust'].units == 'm/s'
    assert response.json()[0] == {
            'lat': 43.08,
            'lon': -89.54,
            'observation_time': {'value': '2020-06-22T20:00:00.000Z'},
            'wind_gust': {'units': 'm/s', 'value': 3.49},
            'precipitation_type': {'value': 'rain'}
            }


@my_vcr.use_cassette('tests/vcr_cassettes/forecast-hourly-with-end-time.yml')
def test_forecast_hourly_with_end_time():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    start_time = datetime(2020, 6, 22, 23, tzinfo=timezone.utc)
    end_time = start_time + timedelta(minutes=60)
    response = api_client.forecast_hourly(
            lat='40', lon='80',
            start_time=start_time.isoformat(), end_time=end_time.isoformat(),
            fields=['wind_gust', 'precipitation_type'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 2
    assert data[0].lat == 40
    assert data[0].lon == 80
    assert data[0].observation_time == dateutil.parser.parse(
            '2020-06-22T23:00:00.000Z')
    measurements = data[0].measurements
    assert measurements['precipitation_type'].value == 'none'
    assert measurements['precipitation_type'].units is None
    assert measurements['wind_gust'].value == 3
    assert measurements['wind_gust'].units == 'm/s'
    assert response.json()[0] == {
            'lat': 40,
            'lon': 80,
            'observation_time': {'value': '2020-06-22T23:00:00.000Z'},
            'wind_gust': {'units': 'm/s', 'value': 3},
            'precipitation_type': {'value': 'none'}
            }


@my_vcr.use_cassette('tests/vcr_cassettes/forecast-daily-no-end-time.yml')
def test_forecast_daily():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    response = api_client.forecast_daily(
            lat='43.08', lon='-89.54', start_time='now', units='us',
            fields=['temp', 'precipitation', 'sunrise'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 15
    assert data[0].lat == 43.08
    assert data[0].lon == -89.54
    assert data[0].observation_time == dateutil.parser.parse('2020-06-23')
    measurements = data[0].measurements
    assert measurements['temp']['min'].value == 52.25
    assert measurements['temp']['min'].units == 'F'
    assert(measurements['temp']['min'].observation_time ==
           dateutil.parser.parse('2020-06-23T11:00:00.000Z'))
    assert measurements['temp']['max'].value == 69.79
    assert measurements['temp']['max'].units == 'F'
    assert(measurements['temp']['max'].observation_time ==
           dateutil.parser.parse('2020-06-23T19:00:00.000Z'))
    assert measurements['precipitation']['max'].value == 0.0271
    assert measurements['precipitation']['max'].units == 'in/hr'
    assert(measurements['precipitation']['max'].observation_time ==
           dateutil.parser.parse('2020-06-23T22:00:00.000Z'))
    assert measurements['sunrise'].value == '2020-06-23T10:19:43.504Z'
    assert response.json()[0] == {
            "temp": [{
                "observation_time": "2020-06-23T11:00:00Z",
                "min": {
                    "value": 52.25,
                    "units": "F"
                }
                },
                {
                "observation_time": "2020-06-23T19:00:00Z",
                "max": {
                    "value": 69.79,
                    "units": "F"
                }
                }
            ],
            "precipitation": [{
                "observation_time": "2020-06-23T22:00:00Z",
                "max": {
                    "value": 0.0271,
                    "units": "in/hr"
                }
            }
            ],
            "sunrise": {
                "value": "2020-06-23T10:19:43.504Z"
            },
            "observation_time": {
                "value": "2020-06-23"
            },
            "lat": 43.08,
            "lon": -89.54,
        }


@my_vcr.use_cassette('tests/vcr_cassettes/forecast-daily-with-end-time.yml')
def test_forecast_daily_with_end_time():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    start_time = datetime(2020, 6, 24, 12, tzinfo=timezone.utc)
    end_time = start_time + timedelta(days=2)
    response = api_client.forecast_daily(
            lat='40', lon='80',
            start_time=start_time.isoformat(), end_time=end_time.isoformat(),
            fields=['temp', 'precipitation', 'sunrise'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 4
    assert data[0].lat == 40
    assert data[0].lon == 80
    assert data[0].observation_time == dateutil.parser.parse('2020-06-23')
    measurements = data[0].measurements
    assert measurements['temp']['min'].value == 26.75
    assert measurements['temp']['min'].units == 'C'
    assert(measurements['temp']['min'].observation_time ==
           dateutil.parser.parse('2020-06-23T23:00:00.000Z'))
    assert measurements['temp']['max'].value == 38.25
    assert measurements['temp']['max'].units == 'C'
    assert(measurements['temp']['max'].observation_time ==
           dateutil.parser.parse('2020-06-23T11:00:00.000Z'))
    assert measurements['precipitation']['max'].value == 0
    assert measurements['precipitation']['max'].units == 'mm/hr'
    assert(measurements['precipitation']['max'].observation_time ==
           dateutil.parser.parse('2020-06-23T07:00:00.000Z'))
    assert measurements['sunrise'].value == '2020-06-22T23:13:04.950Z'
    assert response.json()[0] == {
            "temp": [{
                "observation_time": "2020-06-23T23:00:00Z",
                "min": {
                    "value": 26.75,
                    "units": "C"
                }
                },
                {
                "observation_time": "2020-06-23T11:00:00Z",
                "max": {
                    "value": 38.25,
                    "units": "C"
                }
                }
            ],
            "precipitation": [{
                "observation_time": "2020-06-23T07:00:00Z",
                "max": {
                    "value": 0,
                    "units": "mm/hr"
                }
            }
            ],
            "sunrise": {
                "value": "2020-06-22T23:13:04.950Z"
            },
            "observation_time": {
                "value": "2020-06-23"
            },
            "lat": 40,
            "lon": 80
        }


@my_vcr.use_cassette('tests/vcr_cassettes/historical-climacell.yml')
def test_historical_climacell():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    start_time = datetime(2020, 6, 24, 12, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=4)
    response = api_client.historical_climacell(
            lat='43.08', lon='-89.54', start_time=start_time, timestep=30,
            end_time=end_time,
            fields=['wind_gust', 'precipitation_type', 'sunset'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 9
    assert data[0].lat == 43.08
    assert data[0].lon == -89.54
    assert data[0].observation_time == dateutil.parser.parse(
            '2020-06-24T12:00:00.000Z')
    measurements = data[0].measurements
    assert measurements['precipitation_type'].value == 'none'
    assert measurements['precipitation_type'].units is None
    assert measurements['sunset'].value == '2020-06-25T01:41:48.098Z'
    assert measurements['sunset'].units is None
    assert measurements['wind_gust'].value == 7.5
    assert measurements['wind_gust'].units == 'm/s'
    assert response.json()[0] == {
            'lat': 43.08,
            'lon': -89.54,
            'observation_time': {'value': '2020-06-24T12:00:00.000Z'},
            'wind_gust': {'units': 'm/s', 'value': 7.5},
            'precipitation_type': {'value': 'none'},
            'sunset': {'value': '2020-06-25T01:41:48.098Z'}
            }


@my_vcr.use_cassette('tests/vcr_cassettes/historical-station.yml')
def test_historical_station():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    start_time = datetime(2020, 6, 23, 20, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=4)
    response = api_client.historical_station(
            lat='43.08', lon='-89.54', start_time=start_time,
            end_time=end_time, fields=['temp', 'precipitation_type'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 12
    assert data[0].observation_time == dateutil.parser.parse(
            '2020-06-23T20:15:00.000Z')
    measurements = data[0].measurements
    assert measurements['precipitation_type'].value == 'none'
    assert measurements['precipitation_type'].units is None
    assert measurements['temp'].value == 22.4
    assert measurements['temp'].units == 'C'
    assert response.json()[0] == {
            'observation_time': {'value': '2020-06-23T20:15:00.000Z'},
            'temp': {'units': 'C', 'value': 22.4},
            'precipitation_type': {'value': 'none'}
            }


@my_vcr.use_cassette('tests/vcr_cassettes/insights-fire-index.yml')
def test_insights_fireindex():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    response = api_client.insights_fire_index(lat=43.08, lon=-89.54)

    assert response.status_code == 200
    data = response.data()
    assert data.fire_index == 30.474195
    assert response.json() == [{'fire_index': 30.474195}]
