from datetime import date
import re
from bluetooth import BluetoothSocket, BluetoothError
from datetime import datetime
from serial import SerialException

try:
    from app.clases_varias.connection import M_bluetooth, M_serial
    from app.tools.logger import create_log
    from app.tools.config import *
    from app.tools.flags import *
    from app.clases_varias.ambient import Ambient
except ImportError:
    from clases_varias.connection import M_bluetooth, M_serial
    from tools.logger import create_log
    from tools.config import *
    from tools.flags import *

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


class Element:

    def get_state(self, cnx):
        'Implement in after'


class Dht_22(Element):

    def __init__(self, sensor=1):
        self.sensor = sensor

    def get_state(self) -> Ambient:
        'Return object ambient with temperature, humidity, date and sensor number'

        return Ambient()

    # def read_nano_bluetooth(sock: BluetoothSocket, device: int) -> dict:
    def read_ambient(self, sock: M_bluetooth) -> Ambient:
        ambient = Ambient()
        # sock.recv(1024)

        logger.debug('reading sensor {}'.format(self.sensor))
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

        # logger.debug('sock.get_state():{}'.format(sock.get_state()))

        while True:
            if sock.get_state() == False:
                logger.debug('sock.get_state():{}'.format(sock.get_state()))
                return ambient
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
                sock.state = False
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

    def __init__(self, state=False):
        self.state = state

    def get_state(self, cnx_serial: M_serial):
        self.state = ''

        try:
            state = cnx_serial.read_all()
            state = state.decode('utf-8')

            if (re.search('ON', state)):
                p = re.search('ON', state)
                self.state = p.group()
            elif (re.search('OFF', state)):
                p = re.search('OFF', state)
                self.state = p.group()

        except SerialException as err:
            logger.error(err)
