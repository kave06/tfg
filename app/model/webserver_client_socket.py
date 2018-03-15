import socket
import sys
import os

sys.path.append('../modules')

try:
    from app.modules.logger import create_log
except ImportError:
    from logger import create_log

HOST, PORT = '89.128.192.144', 1100

# APP_DIR = os.path.dirname(os.path.realpath(__file__))
# logger_name = APP_DIR + '/logs/prototype'
# logger = create_log(logger_name)

logger = create_log('prototype')

def led_on_off(state: str):
    # data = " ".join(sys.argv[1:])
    # data = 'ON'.encode()
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
