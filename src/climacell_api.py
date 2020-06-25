import requests
from climacell_response import ClimacellResponse


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
            "end_time": end_time,
            "timestep": timestep,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        response = self._make_request(
                url_suffix="/weather/historical/climacell", params=params)
        return ClimacellResponse(request_response=response, fields=fields)

    def historical_station(self, lat, lon, fields, start_time,
                           end_time='now', units='si'):
        params = {
            "lat": lat,
            "lon": lon,
            "start_time": start_time,
            "end_time": end_time,
            "unit_system": units,
            "fields": ",".join(fields),
            "apikey": self.key
        }

        response = self._make_request(
                url_suffix="/weather/historical/station", params=params)
        return ClimacellResponse(request_response=response, fields=fields)

    def insights_fire_index(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "apikey": self.key
        }

        response = self._make_request(
                url_suffix="/insights/fire-index", params=params)
        return ClimacellResponse(request_response=response, fields=[],
                                 response_type='fire_index')

    def _make_request(self, url_suffix, params):
        return requests.get(self.BASE_URL + url_suffix, params=params)
