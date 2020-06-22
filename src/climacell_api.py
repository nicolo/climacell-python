import dateutil.parser
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

        response = self._make_request(
                url_suffix="/weather/realtime", params=params)
        return ClimacellResponse(request_response=response, fields=fields)

    def _make_request(self, url_suffix, params):
        return requests.get(self.BASE_URL + url_suffix, params=params)


class ClimacellResponse:

    def __init__(self, request_response, fields):
        self.request_response = request_response
        self.fields = fields
        self.json_data = request_response.json()

    @property
    def lat(self):
        return self.json_data.get('lat', None)

    @property
    def lon(self):
        return self.json_data.get('lon', None)

    @property
    def observation_time(self):
        if self.error_code is not None:
            return None

        return dateutil.parser.parse(
                self.json_data['observation_time']['value'])

    @property
    def measurements(self):
        if self.error_code is not None:
            return {}

        m_dict = {}
        for f in self.fields:
            m_dict[f] = Measurement(
                    value=self.json_data[f]['value'],
                    units=self.json_data[f]['units'])
        return m_dict

    @property
    def error_code(self):
        return self.json_data.get('errorCode', None)

    @property
    def error_message(self):
        return self.json_data.get('message', None)

    def __getattr__(self, attrib):
        return getattr(self.request_response, attrib)


class Measurement:

    def __init__(self, value, units):
        self.value = value
        self.units = units
