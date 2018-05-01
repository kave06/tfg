from time import sleep

try:
    from app.clases_varias.socket import Client
    from app.tools.config import *
    from app.clases_varias.element import *
except ImportError:
    from clases_varias.socket import Client
    from tools.config import *
    from clases_varias.element import *


def init_socket_send_relay_state():
    port = webserver_socket_port_relay_state_out
    relay = Relay()
    sock_client = Client(host=webserver_ip, port=port)
    sock_client.connected()

    serial = M_serial()
    serial.connected()
    logger.debug(serial.connection.is_open)
    while True:
        logger.debug('outer while')
        if sock_client.get_state() == False:
            # Connect socket
            # logger.debug('reconnect socket')
            sock_client.sock.close()
            sock_client = Client(host=webserver_ip, port=port)
            sock_client.connected()
        elif serial.connection.is_open == False:
            serial = M_serial()
            serial.connected()
            # logger.debug('cnx_serial_state:{}'.format(serial.connection.is_open))

        while serial.connection.is_open or sock_client.get_state() or sock_client.state:
            # logger.debug(sock_client.get_state())
            relay.get_state(serial)
            try:
                sock_client.sock.sendall(bytes((relay.state).encode()))
                # logger.debug(relay.state)
            except OSError as err:
                sock_client.state = False
                logger.error(err)

            sleep(1)


init_socket_send_relay_state()
