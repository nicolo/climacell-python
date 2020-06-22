from datetime import datetime, timedelta, timezone
import dateutil.parser
import os
import vcr
from climacell_api import ClimacellApiClient

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
