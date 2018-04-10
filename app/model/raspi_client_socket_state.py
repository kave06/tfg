import os
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

APP_DIR = os.getcwd()
logger_name = APP_DIR + '/app/logs/prototype'
try:
    logger = create_log(logger_name)
except:
    logger_name = APP_DIR + '/logs/prototype'
    logger = create_log(logger_name)

HOST, PORT = webserver_ip, webserver_socket_port_relay_state_out


def relay_state():
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
                sock.sendall(bytes(state.encode()))
            except OSError as err:
                logger.error(err)
            finally:
                sock.close()

            sleep(1)
