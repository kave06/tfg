import socket

try:
    from app.tools.logger import create_log
    from app.tools.config import *
except ImportError:
    from tools.logger import create_log
    from tools.config import *

HOST, PORT = raspi_ip, raspi_socket_port_on_off

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


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
