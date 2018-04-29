from serial import Serial, SerialException
from bluetooth import BluetoothSocket, RFCOMM, BluetoothError

from app.tools.config import *
from app.tools.logger import create_log

logger = create_log(webserver_logger)


class Connection():
    'There are several types of connections'

    def connected(self, port):
        print('This is connect but need type of connection')


class M_serial(Serial, Connection):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.connection = False
        # self.is_connected = False

    def connected(self, device=serial_port, baudrate=serial_bd):
        try:
            self.connection = Serial(port=serial_port, baudrate=serial_bd)
            logger.info('connect to serial to port: {}'.format(serial_port))
        except SerialException as err:
            logger.error(err)

    def get_state(self):
        return self.is_open


class M_bluetooth(BluetoothSocket):

    def __init__(self, mac_addr):
        super(self.__class__, self).__init__()
        self.sock = BluetoothSocket(RFCOMM)
        self.mac_addr = mac_addr

    # TODO check errores from nano.py
    def connected(self, port=1):

        try:
            self.sock.connect((self.mac_addr, port))
            logger.info('socket connection successful in device: {}'.format(self.mac_addr))
        except BluetoothError as err:
            logger.error(err)

    def get_state(self):
        no_device = '00:00:00:00:00:00'
        # logger.info('self.sock.readsock:{}'.format(self.sock.connected))
        if self.sock.getsockname()[0] == no_device:
            return False
        return True

    def my_recv(self, numbytes):
        return self.sock.recv(numbytes)

    def get_sock_name(self):
        return self.sock.getsockname()[0]
