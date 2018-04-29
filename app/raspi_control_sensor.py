from time import sleep
from threading import Thread

try:
    from app.model.nano import connect_bluetooth, read_nano_bluetooth, connect_serial, read_serial_state
    from app.model.rabbitMQ import connect_queue_sender, send_queue_ambient
    from app.model.raspi_client_socket_state import relay_state
    from app.tools.logger import create_log
    from app.tools.flags import Flag
    from app.tools.config import *
    from app.clases_varias.connection import *
    from app.clases_varias.element import *
    # from app.tools.manage_file import write_file
except ImportError:
    # from model.nano import connect_bluetooth, read_nano_bluetooth, connect_serial, read_serial_state
    # from model.rabbitMQ import connect_queue_sender, send_queue_ambient
    # from model.raspi_client_socket_state import relay_state
    # from tools.logger import create_log
    # from tools.flags import Flag
    # from tools.config import *
    # from tools.manage_file import write_file
    pass

db_addr1 = bluetooth_module1
db_addr2 = bluetooth_module2
port1 = bluetooth_port1

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


def main():
    # init objects
    sock3 = M_bluetooth(bluetooth_module1)
    sock1 = M_bluetooth(bluetooth_module1)
    sock2 = M_bluetooth(bluetooth_module2)

    sensor1 = Dht_22()
    sensor2 = Dht_22()

    # t1 = Thread(target=relay_state)
    # t1.start()

    sleep(0.1)
    sock1.connected()
    sleep(0.1)
    sock2.connected()

    # relay_state()
    # sleep(0.1)
    # sock1 = connect_bluetooth(db_addr1, port1)
    # sleep(0.1)
    # sock2 = connect_bluetooth(db_addr2, port1)

    while True:

        if sock1.get_state() == False:
            sleep(0.1)
            logger.debug('sock1.get_state(): {}'.format(sock2.get_state()))
            sock1.connected()
        elif sock2.get_state() == False:
            sleep(0.1)
            logger.debug('sock2.get_state(): {}'.format(sock2.get_state()))
            sock2 = M_bluetooth(bluetooth_module2)
            sock2.connected()

        # if Flag.sock_bluetooth1 == False and Flag.sock_bluetooth2 == False:
        #     Flag.sock_bluetooth1 = True
        #     sock1 = connect_bluetooth(db_addr1, port1)
        #     Flag.sock_bluetooth2 = True
        #     sleep(0.1)
        #     sock2 = connect_bluetooth(db_addr2, port1)

        while Flag.inner_while:
            # ambient1 = read_nano_bluetooth(sock1, 1)
            ambient1 = sensor1.read_ambient(sock1)
            ambient2 = sensor2.read_ambient(sock2)
            # logger.info(sock2.get_sock_name())



            cnx = connect_queue_sender()
            send_queue_ambient(cnx, ambient1)
            send_queue_ambient(cnx, ambient2)
            # write_file(file, '{} {}\n'.format(datetime.now(), ambient1))
            sleep(0.1)

            # write_file(file, '{} {}\n'.format(datetime.now(), ambient2))

            if (ambient1.temperature == 100 or ambient2.temperature == 100
                    or sock1.get_state()==False or sock2.get_state()==False):
                Flag.inner_while = False

        Flag.inner_while = True


if __name__ == '__main__':
    main()
