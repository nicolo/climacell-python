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
    assert response.lat == 12
    assert response.lon == 13
    assert response.observation_time == dateutil.parser.parse(
            '2020-06-09T18:53:12.746Z')
    measurements = response.measurements
    assert measurements['temp'].value == 102.2
    assert measurements['temp'].units == 'F'
    assert measurements['wind_gust'].value == 8.68
    assert measurements['wind_gust'].units == 'mph'
    assert response.error_code is None
    assert response.error_message is None
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
    assert response.lat is None
    assert response.lon is None
    assert response.observation_time is None
    assert response.measurements == {}
    assert response.error_code == 'BadRequest'
    assert response.error_message == 'lon must be in the range -180..180'
    assert response.json() == {
            'statusCode': 400,
            'errorCode': 'BadRequest',
            'message': 'lon must be in the range -180..180',
            }
