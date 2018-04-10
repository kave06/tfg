import socket
from time import sleep

try:
    from app.model.nano import read_serial_state, connect_serial
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from model.nano import read_serial_state, connect_serial
    from modules.logger import create_log
    from modules.config import *

logger = create_log('prototype')
HOST, PORT = 'gui.uva.es', 5576


def relay_state_change__():
    while True:
        ser = connect_serial(serial_port, serial_bd)
        while ser.is_open:
            state = read_serial_state(ser)
            print(state)

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # Connect to server and send data
                sock.connect((HOST, PORT))
                sock.sendall(bytes(state))
            except OSError as err:
                logger.error(err)
            finally:
                sock.close()

            sleep(1)
