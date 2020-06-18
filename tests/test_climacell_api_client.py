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
    assert response.json() == {
            'lat': 12,
            'lon': 13,
            'observation_time': {'value': '2020-06-09T18:53:12.746Z'},
            'temp': {'units': 'F', 'value': 102.2},
            'wind_gust': {'units': 'mph', 'value': 8.68}
            }
