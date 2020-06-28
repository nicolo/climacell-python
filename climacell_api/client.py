import requests
from climacell_api.climacell_response import ClimacellResponse


class ClimacellApiClient:
    BASE_URL = "https://api.climacell.co/v3"

    def __init__(self, key):
        self.key = key

    def realtime(self, lat, lon, fields, units='si'):
        """
        The realtime data returns up to the minute observational data for
        specificed location.

        :param float lat: Latitude of location
        :param float lon: Longitude of location
        :param list fields: List of data fields to pull
        :param string units: Either scientific ('si') or US ('us')

        :returns: Request response object with data() as ObservationData
        :rtype: ClimacellResponse
        """

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
        """
        The nowcast endpoint is minute by minute forcasting data for up to 360
        minutes in the future.

        :param float lat: Latitude of location
        :param float lon: Longitude of location
        :param int timestep: Minutes between forecasts
        :param list fields: List of data fields to pull
        :param string start_time: Either 'now' or datetime ISO 8601 string
        :param string end_time: None or ISO 8601 string
        :param string units: Either scientific ('si') or US ('us')

        :returns: Request response object with data() as a list of
        ObservationData
        :rtype: ClimacellResponse
        """

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
        """
        Hourly forcasting data for up to 96 hours in the future.

        :param float lat: Latitude of location
        :param float lon: Longitude of location
        :param list fields: List of data fields to pull
        :param string start_time: Either 'now' or datetime ISO 8601 string
        :param string end_time: None or datetime ISO 8601 string
        :param string units: Either scientific ('si') or US ('us')

        :returns: Request response object with data() as a list of
        DailyObservationData
        :rtype: ClimacellResponse
        """

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
        """
        Daily forcasting data for up to 15 days in the future.

        :param float lat: Latitude of location
        :param float lon: Longitude of location
        :param list fields: List of data fields to pull
        :param string start_time: Either 'now' or datetime ISO 8601 string
        :param string end_time: None or datetime ISO 8601 string
        :param string units: Either scientific ('si') or US ('us')

        :returns: Request response object with data() as a list of
        ObservationData
        :rtype: ClimacellResponse
        """

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
        """
        Historical ClimaCell data for up to 6 hours in the past

        :param float lat: Latitude of location
        :param float lon: Longitude of location
        :param int timestep: Minutes between forecasts
        :param list fields: List of data fields to pull
        :param string start_time: Datetime ISO 8601 string
        :param string end_time: Either 'now' or datetime ISO 8601 string
        :param string units: Either scientific ('si') or US ('us')

        :returns: Request response object with data() as a list of
        ObservationData
        :rtype: ClimacellResponse
        """

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
        """
        Historical weather station data for up to 4 weeks in the past

        :param float lat: Latitude of location
        :param float lon: Longitude of location
        :param int timestep: Minutes between forecasts
        :param list fields: List of data fields to pull
        :param string start_time: Datetime ISO 8601 string
        :param string end_time: Either 'now' or datetime ISO 8601 string
        :param string units: Either scientific ('si') or US ('us')

        :returns: Request response object with data() as a list of
        ObservationData
        :rtype: ClimacellResponse
        """

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
        """
        Historical weather station data for up to 4 weeks in the past

        :param float lat: Latitude of location
        :param float lon: Longitude of location
        :param int timestep: Minutes between forecasts
        :param list fields: List of data fields to pull
        :param string start_time: Datetime ISO 8601 string
        :param string end_time: Either 'now' or datetime ISO 8601 string
        :param string units: Either scientific ('si') or US ('us')

        :returns: Request response object with data() that returns
        FireIndexData
        :rtype: ClimacellResponse
        """

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
