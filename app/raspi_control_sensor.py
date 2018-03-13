from time import sleep

try:
    from app.modules.logger import create_log
    from app.model.database import connect_db
    from app.model.nano import connect_bluetooth, read_nano_bluetooth
    from app.modules.flags import Flag
    from app.model.sender import connect_queue, send_data_queue
except ImportError:
    from modules.logger import create_log
    from model.database import connect_db
    from model.nano import connect_bluetooth, read_nano_bluetooth
    from modules.flags import Flag
    from model.sender import connect_queue, send_data_queue

db_addr1 = '98:D3:33:81:07:B3'
db_addr2 = '98:D3:33:81:07:E8'
port1 = 1

logger = create_log('prototype')


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
