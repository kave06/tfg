from serial import Serial, SerialException
from bluetooth import BluetoothSocket, RFCOMM, BluetoothError
from time import sleep

try:
    from app.tools.config import *
    from app.tools.logger import create_log
except ImportError:
    from tools.config import *
    from tools.logger import create_log

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


class Connection():
    'There are several types of connections'

    def connected(self):
        print('This is connect but need type of connection')


class M_serial(Serial, Connection):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.connection = Serial()
        # self.is_connected = False

    def connected(self, device=serial_port, baudrate=serial_bd):
        try:
            self.connection = Serial(port=serial_port, baudrate=serial_bd)
            logger.info('connect to serial to port: {}'.format(serial_port))
        except SerialException as err:
            logger.error(err)

    def send_signal(self, signal: bytes):
        self.connected()
        sleep(0.5)

        signal = signal.decode()

        try:
            if signal == 'ON':
                self.connection.write('1'.encode())
            elif signal == 'OFF':
                self.connection.write('0'.encode())
            self.connection.close()
        except SerialException as err:
            logger.error(err)

    def get_state(self):
        return self.is_open


class M_bluetooth(BluetoothSocket, Connection):

    def __init__(self, mac_addr):
        super(self.__class__, self).__init__()
        self.sock = BluetoothSocket(RFCOMM)
        self.mac_addr = mac_addr
        self.state = False

    # TODO check errores from nano.py
    def connected(self, port=1):

        try:
            self.sock.connect((self.mac_addr, port))
            self.state = True
            logger.info('socket connection successful in device: {}'.format(self.mac_addr))
        except BluetoothError as err:
            self.state = False
            logger.error(err)

    def get_state(self):
        # no_device = '00:00:00:00:00:00'
        # # logger.info('self.sock.readsock:{}'.format(self.sock.connected))
        # if self.sock.getsockname()[0] == no_device:
        #     return False
        # return True
        return self.state

    def my_recv(self, numbytes):
        return self.sock.recv(numbytes)

    # def get_sock_name(self):
    #     return self.sock.getsockname()[0]

    def reconnect(self):
        sleep(0.1)
        logger.debug('sock1.get_state(): {}'.format(self.get_state()))
        # self.sock.close()
        # sock = M_bluetooth(bluetooth_module1)
        self.connected()
