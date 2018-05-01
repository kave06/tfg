from threading import Thread

try:
    from app.clases_varias.element import *
    from app.clases_varias.connection import *
    from app.clases_varias.rabbitMQ import Sender
    from app.sockets.client_relay_state import relay_state
    from app.tools.config import *
    from app.tools.logger import create_log
except ImportError:
    from clases_varias.element import *
    from clases_varias.connection import *
    from clases_varias.rabbitMQ import Sender
    from sockets.client_relay_state import relay_state
    from tools.config import *
    from tools.logger import create_log

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


def main():
    # init objects
    bluetooth1 = M_bluetooth(bluetooth_module1)
    bluetooth2 = M_bluetooth(bluetooth_module2)

    sensor1 = Dht_22(1)
    sensor2 = Dht_22(2)

    rabbit_sender = Sender()

    # init socket to send relay state
    t1 = Thread(target=relay_state)
    t1.start()

    # Connect Bluetooth socks
    bluetooth1.connected()
    sleep(0.1)
    bluetooth2.connected()

    while True:

        logger.debug('outer while')
        if bluetooth1.get_state() == False:
            sleep(0.1)
            logger.debug('bluetooth1.get_state(): {}'.format(bluetooth1.get_state()))
            bluetooth1.sock.close()
            bluetooth1 = M_bluetooth(bluetooth_module1)
            bluetooth1.connected()
        elif bluetooth2.get_state() == False:
            sleep(0.1)
            logger.debug('bluetooth2.get_state(): {}'.format(bluetooth2.get_state()))
            bluetooth2.sock.close()
            bluetooth2 = M_bluetooth(bluetooth_module2)
            bluetooth2.connected()

        while Flag.inner_while:
            ambient1 = sensor1.read_ambient(bluetooth1)
            ambient2 = sensor2.read_ambient(bluetooth2)

            # Connect to rabbitMQ queue
            rabbit_sender.connected()
            rabbit_sender.send(ambient1)
            rabbit_sender.send(ambient2)
            rabbit_sender.connection.close()

            # write_file(file, '{} {}\n'.format(datetime.now(), ambient1))

            if (ambient1.temperature == 100 or ambient2.temperature == 100
                    or bluetooth1.get_state() == False or bluetooth2.get_state() == False):
                Flag.inner_while = False

        Flag.inner_while = True


if __name__ == '__main__':
    main()
