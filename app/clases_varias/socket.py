import socket
from time import sleep

from app.clases_varias.element import Relay

try:
    from app.model.nano import read_serial_state, connect_serial
    from app.tools.logger import create_log
    from app.tools.config import *
    from app.clases_varias.connection import Connection, M_serial
except ImportError:
    from model.nano import read_serial_state, connect_serial
    from tools.logger import create_log
    from tools.config import *
    from clases_varias.connection import Connection, M_serial

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


# class M_socket(socket, Connection):
class M_socket(Connection):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connected(self):
        pass

    pass

    def get_state(self):
        state = self.sock.fileno()
        if state == -1:
            return False
        else:
            return True


class Client(M_socket):

    def connected(self):
        # HOST, PORT = self.host, self.port
        try:
            self.sock.connect((self.host, self.port))
            logger.info('socket connected successfully')
        except OSError as err:
            logger.error(err)

    def send_relay_state(self):
        relay = Relay()
        logger.debug('hi')

        # Serial connection to connect to relay
        cnx_serial = M_serial()
        cnx_serial.connected()

        while True:
            if self.get_state() == False:
                # Connect socket
                self.connected()
            elif cnx_serial.is_open == False:
                cnx_serial = M_serial()
                cnx_serial.connected()

            while cnx_serial.is_open and self.get_state():
                relay.get_state(cnx_serial)
                try:
                    self.sock.sendall(bytes(relay.state))
                except OSError as err:
                    logger.error(err)
                sleep(1)
