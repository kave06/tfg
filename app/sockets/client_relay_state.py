from time import sleep

try:
    from app.clases_varias.socket import Client
    from app.tools.config import *
    from app.clases_varias.element import *
except ImportError:
    from clases_varias.socket import Client
    from tools.config import *
    from clases_varias.element import *


def relay_state():
    logger.debug('---------------------------------------------------')
    logger.debug('---------------------------------------------------')
    port = webserver_socket_port_relay_state_out
    relay = Relay()
    sock_client = Client(host=webserver_ip, port=port)
    # sock_client.connected()
    sock_client.state = True

    serial = M_serial()
    serial.connected()
    logger.debug(serial.connection.is_open)

    while True:
        logger.debug('outer while')
        # if sock_client.get_state() == False:
        if sock_client.state == False:
            # Connect socket
            logger.debug('reconnect socket')
            sock_client.sock.close()
            sock_client = Client(host=webserver_ip, port=port)
            sock_client.connected()
        elif serial.connection.is_open == False:
            serial = M_serial()
            serial.connected()
            logger.debug('cnx_serial_state:{}'.format(serial.connection.is_open))

        # while serial.connection.is_open and sock_client.get_state() and sock_client.state:
        sleep(0.2)
        while serial.connection.is_open and sock_client.state:
            # logger.debug(sock_client.get_state())
            sock_client = Client(host=webserver_ip, port=port)
            relay.get_state(serial)
            # state = relay.state
            # logger.debug(state)
            sock_client.send_relay_state(relay, serial)

            sleep(time_relay_state)


# relay_state()
