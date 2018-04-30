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
    from app.clases_varias.rabbitMQ import Sender
    # from app.tools.manage_file import write_file
except ImportError:
    from model.nano import connect_bluetooth, read_nano_bluetooth, connect_serial, read_serial_state
    from model.rabbitMQ import connect_queue_sender, send_queue_ambient
    from model.raspi_client_socket_state import relay_state
    from tools.logger import create_log
    from tools.flags import Flag
    from tools.config import *
    from clases_varias.connection import *
    from clases_varias.element import *
    # from tools.manage_file import write_file
    from clases_varias.rabbitMQ import Sender

# db_addr1 = bluetooth_module1
# db_addr2 = bluetooth_module2
# port1 = bluetooth_port1

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


def main():
    # init objects
    sock1 = M_bluetooth(bluetooth_module1)
    sock2 = M_bluetooth(bluetooth_module2)

    sensor1 = Dht_22(1)
    sensor2 = Dht_22(2)

    sender = Sender()

    # t1 = Thread(target=relay_state)
    # t1.start()

    # Connect Bluetooth socks
    sleep(0.1)
    sock1.connected()
    sleep(0.1)
    sock2.connected()

    while True:

        logger.debug('outer while')
        if sock1.get_state() == False:
            sleep(0.1)
            logger.debug('sock1.get_state(): {}'.format(sock1.get_state()))
            sock1.sock.close()
            sock1 = M_bluetooth(bluetooth_module1)
            sock1.connected()
        elif sock2.get_state() == False:
            sleep(0.1)
            logger.debug('sock2.get_state(): {}'.format(sock2.get_state()))
            sock2.sock.close()
            sock2 = M_bluetooth(bluetooth_module2)
            sock2.connected()

        while Flag.inner_while:
            ambient1 = sensor1.read_ambient(sock1)
            ambient2 = sensor2.read_ambient(sock2)

            # Connect to rabbitMQ queue
            sender.connected()
            sender.send(ambient1)
            sender.send(ambient2)
            sender.connection.close()

            # write_file(file, '{} {}\n'.format(datetime.now(), ambient1))
            # sleep(0.1)

            if (ambient1.temperature == 100 or ambient2.temperature == 100
                    or sock1.get_state() == False or sock2.get_state() == False):
                Flag.inner_while = False

        Flag.inner_while = True


if __name__ == '__main__':
    main()
