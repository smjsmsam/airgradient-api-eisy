import udi_interface
import requests
import json

LOGGER = udi_interface.LOGGER
Custom = udi_interface.custom

class AirGradientController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(AirGradientController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = name
        self.address = address
        self.primary = primary
        
        self.Notices = Custom(polyglot, 'notices')
        self.Parameters = Custom(polyglot, 'customparams')
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parse)
        self.token = self.Parameters(['Token'])
        
        self.data = ""


    def parse(self):
        return #TODO: if token empty, log error


    def request(self):
        response_API = requests.get(f'https://api.airgradient.com/public/api/v1/locations/measures/current?token={self.token}')
        
        if response_API.status_code == 200:
            parse_json = json.loads(response_API.text)
            self.data = parse_json[self.this_airgradient]
        else:
            LOGGER.error('Not online. {}'.format(response_API.status_code))
        
    #TODO: data grabbing functions are unnecessary
    def all_data(self):
        self.request() #TODO: shortPoll makes this unnecessary
        return self.data
    

    def data_keys(self):
        self.request()
        return self.data.keys()   # json format = dict


    def locationId(self):
        self.request()
        return self.data['locationId']


    def locationName(self):
        self.request()
        return self.data['locationName']


    def co2(self):
        self.request()
        return self.data['rco2']
