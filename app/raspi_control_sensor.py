from time import sleep
import os
from threading import Thread
from datetime import datetime

try:
    from app.model.nano import connect_bluetooth, read_nano_bluetooth, connect_serial, read_serial_state
    from app.model.rabbitMQ import connect_queue_sender, send_queue_ambient
    from app.model.raspi_relay_state import relay_state_______
    from app.model.raspi_client_socket_state import relay_state
    from app.modules.logger import create_log
    from app.modules.flags import Flag
    from app.modules.config import *
    from app.modules.manage_file import write_file
except ImportError:
    from model.nano import connect_bluetooth, read_nano_bluetooth, connect_serial, read_serial_state
    from model.rabbitMQ import connect_queue_sender, send_queue_ambient
    from model.relay_state import relay_state
    from modules.logger import create_log
    from modules.flags import Flag
    from modules.config import *
    from modules.manage_file import write_file

db_addr1 = bluetooth_module1
db_addr2 = bluetooth_module2
port1 = bluetooth_port1

# APP_DIR = os.getcwd()
# logger_name = APP_DIR + '/logs/prototype'
# logger = create_log(logger_name)


logger = create_log('logs/' + name_logger)


def main():
    # path = os.getcwd()
    # file = path + '/logs/ambient'

    t1 = Thread(target=relay_state)
    t1.start()
    # relay_state()
    sleep(0.1)
    sock1 = connect_bluetooth(db_addr1, port1)
    sleep(0.1)
    sock2 = connect_bluetooth(db_addr2, port1)

    while True:

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

        while Flag.inner_while:
            ambient1 = read_nano_bluetooth(sock1, 1)
            cnx = connect_queue_sender()
            send_queue_ambient(cnx, ambient1)
            # write_file(file, '{} {}\n'.format(datetime.now(), ambient1))
            sleep(0.1)

            ambient2 = read_nano_bluetooth(sock2, 2)
            cnx = connect_queue_sender()
            send_queue_ambient(cnx, ambient2)
            # write_file(file, '{} {}\n'.format(datetime.now(), ambient2))


            if (Flag.sock_bluetooth1 == False or Flag.sock_bluetooth2 == False):
                Flag.inner_while = False

        Flag.inner_while = True


if __name__ == '__main__':
    main()
