import dateutil.parser


class ClimacellResponse:
    """
    Wrapper around requests response object that includes a data() method that
    returns all ClimaCell specific data for the endpoint.

    Methods like json() and status_code are delegated to the requests response
    object initialized with the ClimacellResponse object
    """

    def __init__(self, request_response, fields, response_type='forecast'):
        self.request_response = request_response
        self.fields = fields
        self.response_type = response_type

    def data(self):
        raw_json = self.request_response.json()
        if self.status_code != 200:
            return ErrorData(raw_json)

        if self.response_type == 'realtime':
            return ObservationData(raw_json, self.fields)
        elif self.response_type == 'fire_index':
            return FireIndexData(raw_json)
        elif self.response_type == 'daily_forecast':
            observations = []
            for o_json in raw_json:
                observations.append(DailyObservationData(o_json, self.fields))
            return observations
        else:
            observations = []
            for o_json in raw_json:
                observations.append(ObservationData(o_json, self.fields))
            return observations

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


class FireIndexData:

    def __init__(self, raw_json):
        self.raw_json = raw_json

    @property
    def fire_index(self):
        return self.raw_json[0].get('fire_index', None)


class Measurement:

    def __init__(self, value, units, observation_time=None):
        self.value = value
        self.units = units
        self.observation_time = observation_time
