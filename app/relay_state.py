from time import sleep
import os

try:
    from app.model.nano import connect_serial, read_serial_state
    from app.model.sender import connect_queue, send_queue_ambient, send_queue_relay
    from app.modules.logger import create_log
    from app.modules.flags import Flag
    from app.modules.config import *
except ImportError:
    from model.nano import connect_serial, read_serial_state
    from model.sender import connect_queue, send_queue_ambient, send_queue_relay
    from modules.logger import create_log
    from modules.flags import Flag
    from modules.config import *

# APP_DIR = os.path.dirname(os.path.realpath(__file__))
# logger_name = APP_DIR + '/logs/relay_state'
logger = create_log('relay_state')


def relay_state():
    while True:

        ser = connect_serial(serial_port, serial_bd)
        cnx = connect_queue()

        while Flag.serial and Flag.rabbit_cnx_relay_state:
            state = read_serial_state(ser)
            # logger.debug(state)
            send_queue_relay(cnx, rabbit_queue_relay_state, state)
            sleep(0.5)

        Flag.serial = True
        Flag.rabbit_cnx_relay_state = True

def main():
    relay_state()


if __name__ == '__main__':
   main()