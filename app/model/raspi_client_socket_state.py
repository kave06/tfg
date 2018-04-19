import socket
from time import sleep

try:
    from app.model.nano import read_serial_state, connect_serial
    from app.tools.logger import create_log
    from app.tools.config import *
except ImportError:
    from model.nano import read_serial_state, connect_serial
    from tools.logger import create_log
    from tools.config import *

HOST, PORT = webserver_ip, webserver_socket_port_relay_state_out

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


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
