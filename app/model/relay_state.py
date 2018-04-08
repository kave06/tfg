import os
from time import sleep
from datetime import datetime

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
logger = create_log('prototype')


def relay_state():
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    path = APP_DIR + '/../logs/'
    file_relay_state = path + 'relay_state'
    f = open(file_relay_state,'w')
    while True:

        ser = connect_serial(serial_port, serial_bd)
        cnx = connect_queue_sender()

        while Flag.serial and cnx.is_open:
            state = read_serial_state(ser)
            # logger.debug(state)
            send_queue_relay(cnx, state)
            try:
                f.write('{} -- {}\n'.format( datetime.now(), state))
                f.flush()
            except Exception as err:
                logger.error(err)
            sleep(1)

        try:
            # cnx.close()
            ser.close()
        except Exception as err:
            logger.error(err)

        # try:
        #     ser.close()
        # except Exception as err:
        #     logger.error(err)
        Flag.serial = True
        # Flag.rabbit_cnx_relay_state = True




# def count_state():
#     relay_state()
#
#
# if __name__ == '__main__':
#    count_state()