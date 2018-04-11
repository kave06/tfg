import os
import socket

try:
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from modules.logger import create_log
    from modules.config import *

HOST, PORT = raspi_ip, raspi_socket_port_on_off

# APP_DIR = os.getcwd()
# logger_name = APP_DIR + '/app/logs/prototype'
# try:
#     logger = create_log(logger_name)
# except:
#     logger_name = APP_DIR + '/logs/prototype'
#     logger = create_log(logger_name)

# logger_name = '/home/kave/1tfg/prototipo/tfg/app/logs/prototype'
# logger = create_log(logger_name)
#
# try:
#     logger = create_log('app/logs/prototype')
# except:
#     logger = create_log('logs/prototype')

try:
    logger = create_log('app/logs/' + name_logger)
except:
    logger = create_log('logs/' + name_logger)

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
