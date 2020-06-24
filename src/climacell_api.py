import dateutil.parser
import requests


class ClimacellApiClient:
    BASE_URL = "https://api.climacell.co/v3"

    def __init__(self, key):
        self.key = key

    def realtime(self, lat, lon, fields, units='si'):
        params = {
            "lat": lat,
            "lon": lon,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        response = self._make_request(
                url_suffix="/weather/realtime", params=params)
        return ClimacellResponse(request_response=response, fields=fields,
                                 response_type='realtime')

    def nowcast(self, lat, lon, timestep, fields,
                start_time='now', end_time=None, units='si'):
        params = {
            "lat": lat,
            "lon": lon,
            "timestep": timestep,
            "start_time": start_time,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        if end_time is not None:
            params["end_time"] = end_time

        response = self._make_request(
                url_suffix="/weather/nowcast", params=params)
        return ClimacellResponse(request_response=response, fields=fields)

    def forecast_hourly(self, lat, lon, fields, start_time='now',
                        end_time=None, units='si'):
        params = {
            "lat": lat,
            "lon": lon,
            "start_time": start_time,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        if end_time is not None:
            params["end_time"] = end_time

        response = self._make_request(
                url_suffix="/weather/forecast/hourly", params=params)
        return ClimacellResponse(request_response=response, fields=fields)

    def forecast_daily(self, lat, lon, fields, start_time='now',
                       end_time=None, units='si'):
        params = {
            "lat": lat,
            "lon": lon,
            "start_time": start_time,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        if end_time is not None:
            params["end_time"] = end_time

        response = self._make_request(
                url_suffix="/weather/forecast/daily", params=params)
        return ClimacellResponse(request_response=response, fields=fields,
                                 response_type='daily_forecast')

    def historical_climacell(self, lat, lon, fields, timestep, start_time,
                             end_time='now', units='si'):
        params = {
            "lat": lat,
            "lon": lon,
            "start_time": start_time,
            "end_time": start_time,
            "timestep": timestep,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        if end_time is not None:
            params["end_time"] = end_time

        response = self._make_request(
                url_suffix="/weather/historical/climacell", params=params)
        return ClimacellResponse(request_response=response, fields=fields)

    def historical_station(self, lat, lon, fields, start_time,
                           end_time='now', units='si'):
        params = {
            "lat": lat,
            "lon": lon,
            "start_time": start_time,
            "end_time": start_time,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        if end_time is not None:
            params["end_time"] = end_time

        response = self._make_request(
                url_suffix="/weather/historical/station", params=params)
        return ClimacellResponse(request_response=response, fields=fields)

    def _make_request(self, url_suffix, params):
        return requests.get(self.BASE_URL + url_suffix, params=params)


class ClimacellResponse:

    def __init__(self, request_response, fields, response_type='forecast'):
        self.request_response = request_response
        self.fields = fields
        self.response_type = response_type

    def data(self):
        raw_json = self.request_response.json()
        if self.status_code == 200 and self.response_type == 'realtime':
            return ObservationData(raw_json, self.fields)
        elif self.status_code == 200:
            observations = []
            if self.response_type == 'daily_forecast':
                data_class = DailyObservationData
            else:
                data_class = ObservationData
            for o_json in raw_json:
                observations.append(data_class(o_json, self.fields))

            return observations
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


class ObservationData:

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
                    value=self.raw_json[f].get('value', None),
                    units=self.raw_json[f].get('units', None))
        return m_dict


class DailyObservationData(ObservationData):

    @property
    def measurements(self):
        m_dict = {}
        for f in self.fields:
            field_json = self.raw_json[f]
            if isinstance(field_json, list):
                m_dict[f] = {}
                for min_max in field_json:
                    key = 'max' if 'max' in min_max else 'min'
                    value = min_max[key].get('value', None)
                    units = min_max[key].get('units', None)
                    time = dateutil.parser.parse(min_max['observation_time'])
                    m_dict[f][key] = Measurement(value, units, time)
            else:
                m_dict[f] = Measurement(
                    value=field_json.get('value', None),
                    units=field_json.get('units', None))
        return m_dict


class Measurement:

    def __init__(self, value, units, observation_time=None):
        self.value = value
        self.units = units
        self.observation_time = observation_time
