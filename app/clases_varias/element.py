from datetime import date
import re
from bluetooth import BluetoothSocket, BluetoothError
from datetime import datetime

try:
    from app.clases_varias.connection import M_bluetooth
    from app.tools.logger import create_log
    from app.tools.config import *
    from app.tools.flags import *
except ImportError:
    from clases_varias.connection import M_bluetooth
    from tools.logger import create_log
    from tools.config import *
    from tools.flags import *


logger = create_log(raspi_logger)

class Element:

    def get_state(self):
        'Implement in after'


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


class Dht_22(Element):

    def get_state(self) -> Ambient:
        'Return object ambient with temperature, humidity, date and sensor number'

        return Ambient()

    # def read_nano_bluetooth(sock: BluetoothSocket, device: int) -> dict:
    def read_ambient(self, sock: M_bluetooth) -> Ambient:
        ambient = Ambient()
        # sock.recv(1024)

        logger.debug('reading arduino {}'.format(sock.mac_addr))
        regex = '(\d{1}\s\T:\s\d{1,2}\.\d{2}\s\d{2}\.\d{2}\s:H)'
        regex1 = 'nan'
        regex = re.compile(regex)
        regex1 = re.compile(regex1)
        data = ''
        data1 = ''
        # ambient = dict(sensor=0, temperature=100.0, humidity=0.0)
        # ambient.sensor = 0
        # ambient.temperature = 100
        # ambient.humidity = 0

        # try:
        #     sock.getpeername()
        # except BluetoothError as err:
        #     logger.error(err)
        #     Flag.inner_while = False
        #     if device == 1:
        #         Flag.sock_bluetooth1 = False
        #     elif device == 2:
        #         Flag.sock_bluetooth2 = False
        #     logger.debug('return ambient: {}'.format(ambient))
        #     return ambient

        logger.debug('sock.get_state():{}'.format(sock.get_state()))
        if sock.get_state() == False:
            logger.debug('sock.get_state():{}'.format(sock.get_state()))
            return ambient

        while True:
            try:
                data = sock.my_recv(1024)
                # logger.debug(data)
                data = data.decode('unicode_escape')

                # if not receive any data from Arduino
                if re.search(regex1, data):
                    logger.info('data nan')
                    return ambient
            except BluetoothError as err:
                logger.error(err)
                # Flag.inner_while = False
                # logger.debug('return ambient: {}'.format(ambient))
                logger.debug('sensor:{} date:{} temperature:{} humidity:{}'
                             .format(ambient.sensor, ambient.date, ambient.temperature, ambient.humidity))
                return ambient

            data1 = data1 + data

            if re.search(regex, data1):
                m = re.search(regex, data1)
                line = m.group()
                list_values = line.split()
                ambient.sensor = list_values[0]
                ambient.date = datetime.now()
                ambient.temperature = list_values[2]
                ambient.humidity = list_values[3]
                data1 = ''
                # logger.debug('return ambient: {}'.format(ambient))
                # logger.debug('return ambient: {}'.format(ambient.print()))
                logger.debug('sensor:{} date:{} temperature:{} humidity:{}'
                             .format(ambient.sensor, ambient.date, ambient.temperature, ambient.humidity))
                return ambient


class Relay(Element):

    def get_state(self):
        'Return state of relay'

        return 'state is...'
