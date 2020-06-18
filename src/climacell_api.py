import requests


class ClimacellApiClient:
    BASE_URL = "https://api.climacell.co/v3"

    def __init__(self, key):
        self.key = key

    def realtime(self, lat, lon, fields, units='us'):
        params = {
            "lat": lat,
            "lon": lon,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        return self.make_request(url_suffix="/weather/realtime", params=params)

    def make_request(self, url_suffix, params):
        return requests.get(self.BASE_URL + url_suffix, params=params)
