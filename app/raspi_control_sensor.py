from configparser import ConfigParser
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


# config = ConfigParser()
# config.sections()
# config.read('config.ini')
# config.sections()
# bluetooth_config = config['bluetooth']

db_addr1 = '98:D3:33:81:07:B3'
db_addr2 = '98:D3:33:81:07:E8'
port1 = 1

# db_addr1 = bluetooth_config['module1']
# db_addr2 = bluetooth_config['module2']
# port1 = int(bluetooth_config['port1'])
# port2 = int(bluetooth_config['port2'])

logger = create_log('prototype')


def main():
    # cnx = connect_db()
    sleep(0.1)
    sock1 = connect_bluetooth(db_addr1, port1)
    sleep(0.1)
    sock2 = connect_bluetooth(db_addr2, port1)

    while True:
        # logger.info('into outer while')

        # while Flag.connect_db and Flag.sock_bluetooth1:

        if Flag.connect_db == False:
            # logger.info('If connect_db')
            Flag.connect_db = True
            # cnx = connect_db()
        elif Flag.sock_bluetooth1 == False:
            # logger.info('If sock_bluetooth1')
            Flag.sock_bluetooth1 = True
            sleep(0.1)
            sock1 = connect_bluetooth(db_addr1, port1)
        elif Flag.sock_bluetooth2 == False:
            # logger.info('If sock_bluetooth2')
            Flag.sock_bluetooth2 = True
            sleep(0.1)
            sock2 = connect_bluetooth(db_addr2, port1)

        if Flag.sock_bluetooth1 == False and Flag.sock_bluetooth2 == False:
            Flag.sock_bluetooth1 = True
            sock1 = connect_bluetooth(db_addr1, port1)
            Flag.sock_bluetooth2 = True
            sleep(0.1)
            sock2 = connect_bluetooth(db_addr2, port1)

        # logger.info('Before inner while ')
        # logger.info('Flag.connect_db:\t\t{}'.format(Flag.connect_db))
        # logger.info('Flag.sock_bluetooth1:\t{}'.format(Flag.sock_bluetooth1))
        # logger.info('Flag.sock_bluetooth2:\t{}'.format(Flag.sock_bluetooth2))
        # logger.info('Flag.inner_while:\t{}'.format(Flag.inner_while))


        # while Flag.nano_read and Flag.send_data and Flag.connect_db \
        while Flag.connect_db and Flag.inner_while:
            # and (Flag.sock_bluetooth1 or Flag.sock_bluetooth2)\
            # logger.info('----------------Into inner while----------------')

            ambient1 = read_nano_bluetooth(sock1, 1)
            connection_queue = connect_queue()
            send_data_queue(connection_queue,ambient1)
            # send_data(cnx, ambient1)
            sleep(0.1)
            ambient2 = read_nano_bluetooth(sock2, 2)
            connection_queue = connect_queue()
            send_data_queue(connection_queue,ambient2)
            # send_data(cnx, ambient2)

            # logger.info('sensor: {}'.format(ambient1['sensor']))
            # logger.info('temp: {}'.format(ambient1['temperature']))
            # logger.info('humi: {}'.format(ambient1['humidity']))
            # logger.info('sensor: {}'.format(ambient2['sensor']))
            # logger.info('temp: {}'.format(ambient2['temperature']))
            # logger.info('humi: {}'.format(ambient2['humidity']))

            if (Flag.sock_bluetooth1 == False or Flag.sock_bluetooth2 == False):
                Flag.inner_while = False

            # logger.info('Inner while ')
            # logger.info('Flag.connect_db:\t\t{}'.format(Flag.connect_db))
            # logger.info('Flag.sock_bluetooth1:\t{}'.format(Flag.sock_bluetooth1))
            # logger.info('Flag.sock_bluetooth2:\t{}'.format(Flag.sock_bluetooth2))
            # logger.info('Flag.inner_while:\t{}'.format(Flag.inner_while))

            # Flag.nano_read = True
            # Flag.send_data = True



        # logger.info('Outer while ')
        # logger.info('Flag.connect_db:\t\t{}'.format(Flag.connect_db))
        # logger.info('Flag.sock_bluetooth1:\t{}'.format(Flag.sock_bluetooth1))
        # logger.info('Flag.sock_bluetooth2:\t{}'.format(Flag.sock_bluetooth2))
        # logger.info('Flag.inner_while:\t{}'.format(Flag.inner_while))

        Flag.inner_while = True


if __name__ == '__main__':
    main()
