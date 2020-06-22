from datetime import datetime, timedelta, timezone
import dateutil.parser
import os
import vcr
from climacell_api import ClimacellApiClient

my_vcr = vcr.VCR(filter_query_parameters=[('apikey', 'CLIMACELL_API_KEY')])


@my_vcr.use_cassette('tests/vcr_cassettes/real-time-lat12-lon13.yml')
def test_real_time():
    api_client = ClimacellApiClient(key=os.getenv('CLIMACELL_KEY'))
    response = api_client.realtime(
            lat='12', lon='13', fields=['wind_gust', 'temp'])

    assert response.status_code == 200
    data = response.data()
    assert data.lat == 12
    assert data.lon == 13
    assert data.observation_time == dateutil.parser.parse(
            '2020-06-09T18:53:12.746Z')
    measurements = data.measurements
    assert measurements['temp'].value == 102.2
    assert measurements['temp'].units == 'F'
    assert measurements['wind_gust'].value == 8.68
    assert measurements['wind_gust'].units == 'mph'
    assert response.json() == {
            'lat': 12,
            'lon': 13,
            'observation_time': {'value': '2020-06-09T18:53:12.746Z'},
            'temp': {'units': 'F', 'value': 102.2},
            'wind_gust': {'units': 'mph', 'value': 8.68}
            }


@my_vcr.use_cassette('tests/vcr_cassettes/real-time-bad-lon.yml')
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
            lat='40', lon='80', timestep=30, start_time='now',
            fields=['wind_gust', 'precipitation_type'])

    assert response.status_code == 200
    data = response.data()
    assert len(data) == 13
    assert data[0].observation_time == dateutil.parser.parse(
            '2020-06-22T19:07:07.929Z')
    measurements = data[0].measurements
    assert measurements['precipitation_type'].value == 'none'
    assert measurements['precipitation_type'].units is None
    assert measurements['wind_gust'].value == 13.42
    assert measurements['wind_gust'].units == 'mph'
    assert response.json()[0] == {
            'lat': 40,
            'lon': 80,
            'observation_time': {'value': '2020-06-22T19:07:07.929Z'},
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
    assert measurements['wind_gust'].value == 6.71
    assert measurements['wind_gust'].units == 'mph'
    assert response.json()[0] == {
            'lat': 40,
            'lon': 80,
            'observation_time': {'value': '2020-06-22T23:00:00.000Z'},
            'wind_gust': {'units': 'mph', 'value': 6.71},
            'precipitation_type': {'value': 'none'}
            }
