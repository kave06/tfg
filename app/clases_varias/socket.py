import socket
from time import sleep

try:
    from app.tools.logger import create_log
    from app.tools.config import *
    from app.clases_varias.connection import Connection, M_serial
    from app.clases_varias.element import Relay
except ImportError:
    from tools.logger import create_log
    from tools.config import *
    from clases_varias.connection import Connection, M_serial
    from clases_varias.element import Relay

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
        self.state = False

    def connected(self):
        pass

    def get_state(self):
        try:
            self.sock.getpeername()
            self.state = True
            logger.debug(self.sock.getpeername())
            return True
        except OSError as err:
            self.state = False
            logger.error(err)
            return False


class Client(M_socket):

    def connected(self):
        # HOST, PORT = self.host, self.port
        try:
            self.sock.connect((self.host, self.port))
            self.state = True
            # logger.info('socket connected successfully')
        except OSError as err:
            logger.error(err)

    def send_relay_state(self, relay: Relay, cnx: M_serial):
        # relay.get_state(cnx)
        try:
            self.connected()
            self.sock.sendall(bytes((relay.state).encode()))
            self.sock.close()
        except OSError as err:
            self.state = False
            logger.error(err)
