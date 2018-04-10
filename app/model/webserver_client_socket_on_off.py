import socket
import sys

try:
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from modules.logger import create_log
    from modules.config import *

HOST, PORT = raspi_ip, raspi_socket_port_on_off

logger = create_log('prototype')


def relay_on_off(state: str):
    data = state.encode()

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data))
    except OSError as err:
        logger.error(err)
    finally:
        sock.close()
