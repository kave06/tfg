class Ambient():
    'Represent data from sensor with temperature and humidity'

    def __init__(self, sensor_number=0, date=0, temperature=100, humidity=0):
        self.sensor = sensor_number
        self.date = date
        self.temperature = temperature
        self.humidity = humidity

    def print(self):
        print('sensor:{} date:{} temperature:{} humidity:{}'
              .format(self.sensor, self.date, self.temperature, self.humidity))
