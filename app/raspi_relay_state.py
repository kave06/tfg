from time import sleep
import os

try:
    from app.modules.logger import create_log
    # from app.model.database import connect_db
    from app.model.nano import connect_serial, read_serial_state
    from app.model.sender import connect_queue, send_queue_ambient
    from app.modules.flags import Flag
    from app.modules.config import *
except ImportError:
    from modules.logger import create_log
    # from model.database import connect_db
    from model.nano import connect_serial, read_serial_state
    from model.sender import connect_queue, send_queue_ambient
    from modules.flags import Flag
    from modules.config import *


APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/logs/relay_state'
logger = create_log(logger_name)


def main():
    # ser = connect_serial(serial_port, serial_bd)

    while True:

        Flag.serial = True
        ser = connect_serial(serial_port, serial_bd)

        while Flag.serial:
            state_relay = read_serial_state(ser)
            logger.debug(state_relay)
            # TODO develop queue and send state
            cnx_queue_relay = connect_queue()
            send_queue_ambient(cnx_queue_relay, rabbit_queue_relay_state, state_relay)
            # sleep(0.3)


if __name__ == '__main__':
    main()
