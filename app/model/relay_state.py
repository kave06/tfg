from time import sleep
import os

try:
    from app.model.nano import connect_serial, read_serial_state
    from app.model.rabbitMQ import connect_queue_sender, send_queue_relay
    from app.modules.logger import create_log
    from app.modules.flags import Flag
    from app.modules.config import *
except ImportError:
    from model.nano import connect_serial, read_serial_state
    from model.rabbitMQ import connect_queue_sender, send_queue_relay
    from modules.logger import create_log
    from modules.flags import Flag
    from modules.config import *

# APP_DIR = os.path.dirname(os.path.realpath(__file__))
# logger_name = APP_DIR + '/logs/relay_state'
logger = create_log('producer')


def relay_state():
    while True:

        ser = connect_serial(serial_port, serial_bd)
        cnx = connect_queue_sender()

        while Flag.serial and Flag.rabbit_cnx_relay_state:
            state = read_serial_state(ser)
            # logger.debug(state)
            send_queue_relay(cnx, state)
            sleep(1)

        try:
            cnx.close()
            ser.close()
        except Exception as err:
            logger.error(err)

        # try:
        #     ser.close()
        # except Exception as err:
        #     logger.error(err)
        Flag.serial = True
        Flag.rabbit_cnx_relay_state = True

# def count_state():
#     relay_state()
#
#
# if __name__ == '__main__':
#    count_state()