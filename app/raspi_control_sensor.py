from time import sleep
import os

try:
    from app.modules.logger import create_log
    from app.model.database import connect_db
    from app.model.nano import connect_bluetooth, read_nano_bluetooth
    from app.modules.flags import Flag
    from app.model.sender import connect_queue, send_data_queue
    from app.modules.config import *
except ImportError:
    from modules.logger import create_log
    from model.database import connect_db
    from model.nano import connect_bluetooth, read_nano_bluetooth
    from modules.flags import Flag
    from model.sender import connect_queue, send_data_queue
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

    while True:

        if Flag.connect_db == False:
            Flag.connect_db = True
        elif Flag.sock_bluetooth1 == False:
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

        while Flag.connect_db and Flag.inner_while:

            ambient1 = read_nano_bluetooth(sock1, 1)
            connection_queue = connect_queue()
            send_data_queue(connection_queue, ambient1)
            sleep(0.1)

            ambient2 = read_nano_bluetooth(sock2, 2)
            connection_queue = connect_queue()
            send_data_queue(connection_queue, ambient2)

            if (Flag.sock_bluetooth1 == False or Flag.sock_bluetooth2 == False):
                Flag.inner_while = False

        Flag.inner_while = True


if __name__ == '__main__':
    main()
