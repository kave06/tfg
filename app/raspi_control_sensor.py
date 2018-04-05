from time import sleep
import os

try:
    from app.modules.logger import create_log
    # from app.model.database import connect_db
    from app.model.nano import connect_bluetooth, read_nano_bluetooth, connect_serial, read_serial_state
    from app.model.sender import connect_queue, send_queue_ambient
    from app.modules.flags import Flag
    from app.modules.config import *
except ImportError:
    from modules.logger import create_log
    # from model.database import connect_db
    from model.nano import connect_bluetooth, read_nano_bluetooth
    from model.sender import connect_queue, send_queue_ambient
    from modules.flags import Flag
    from modules.config import *

db_addr1 = bluetooth_module1
db_addr2 = bluetooth_module2
port1 = bluetooth_port1

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/logs/prototype'
logger = create_log(logger_name)


def main():
    sleep(0.1)
    sock1 = connect_bluetooth(db_addr1, port1)
    sleep(0.1)
    sock2 = connect_bluetooth(db_addr2, port1)
    ser = connect_serial(serial_port, serial_bd)

    while True:

        # if Flag.connect_db == False:
        #     Flag.connect_db = True
        if Flag.sock_bluetooth1 == False:
            Flag.sock_bluetooth1 = True
            sleep(0.1)
            sock1 = connect_bluetooth(db_addr1, port1)
        elif Flag.sock_bluetooth2 == False:
            Flag.sock_bluetooth2 = True
            sleep(0.1)
            sock2 = connect_bluetooth(db_addr2, port1)

        if Flag.sock_bluetooth1 == False and Flag.sock_bluetooth2 == False:
            Flag.sock_bluetooth1 = True
            sock1 = connect_bluetooth(db_addr1, port1)
            Flag.sock_bluetooth2 = True
            sleep(0.1)
            sock2 = connect_bluetooth(db_addr2, port1)

        if Flag.serial == False:
            Flag.serial = True
            ser = connect_serial(serial_port, serial_bd)

        while Flag.inner_while:
            ambient1 = read_nano_bluetooth(sock1, 1)
            connection_queue_ambient = connect_queue()
            send_queue_ambient(connection_queue_ambient, rabbit_queue_ambient, ambient1)
            sleep(0.1)

            ambient2 = read_nano_bluetooth(sock2, 2)
            connection_queue_ambient = connect_queue()
            send_queue_ambient(connection_queue_ambient,rabbit_queue_ambient, ambient2)

            state_relay = read_serial_state(ser)
            logger.debug(state_relay)
            #TODO develop queue and send state
            cnx_queue_relay = connect_queue()
            send_queue_ambient(cnx_queue_relay, rabbit_queue_relay_state, state_relay)


            if (Flag.sock_bluetooth1 == False or Flag.sock_bluetooth2 == False):
                Flag.inner_while = False

        Flag.inner_while = True


if __name__ == '__main__':
    main()
