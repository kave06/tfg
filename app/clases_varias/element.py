from datetime import date


class Element:


    def get_state(self):
        'Implement in after'


class Ambient():
    'Represent data from sensor with temperature and humidity'
    def __init__(self, sensor_number, date, temperature, humidity):
        self.sensor = sensor_number
        self.date = date
        self.temperature = temperature
        self.humidity = humidity


class dht_22(Element):

    def get_state(self)->Ambient:
        'Return object ambient with temperature, humidity, date and sensor number'

        return Ambient()


class reley(Element):

    def get_state(self):
        'Return state of relay'

        return 'state is...'
