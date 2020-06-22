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

    def data(self):
        raw_json = self.request_response.json()
        if self.status_code == 200:
            return RealtimeData(raw_json, self.fields)
        else:
            return ErrorData(raw_json)

    def __getattr__(self, attrib):
        return getattr(self.request_response, attrib)


class ErrorData:

    def __init__(self, raw_json):
        self.raw_json = raw_json

    @property
    def error_code(self):
        return self.raw_json['errorCode']

    @property
    def error_message(self):
        return self.raw_json['message']


class RealtimeData:

    def __init__(self, raw_json, fields):
        self.raw_json = raw_json
        self.fields = fields

    @property
    def lat(self):
        return self.raw_json.get('lat')

    @property
    def lon(self):
        return self.raw_json.get('lon')

    @property
    def observation_time(self):
        return dateutil.parser.parse(
                self.raw_json['observation_time']['value'])

    @property
    def measurements(self):
        m_dict = {}
        for f in self.fields:
            m_dict[f] = Measurement(
                    value=self.raw_json[f]['value'],
                    units=self.raw_json[f]['units'])
        return m_dict


class Measurement:

    def __init__(self, value, units):
        self.value = value
        self.units = units
