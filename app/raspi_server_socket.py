import socketserver
# from socket import socket
# import socket
# from configparser import ConfigParser

from app.modules.logger import create_log
from app.model.nano import send_signal
# from modules.logger import create_log
# from model.nano import send_signal

# config = ConfigParser()
# config.sections()
# config.read('config.ini')
# config.sections()
# serial_config = config['serial']

# PORT = serial_config['port']
# BD = int(serial_config['bd'])

PORT = '/dev/ttyUSB0'
BD = 9600

logger = create_log('socket.log')


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Escucha la señal que se le manda para encender y apagar el LED.

    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        logger.info('Escuchando')
        # self.request.sendall(self.data)

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        logger.info(self.data)

        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

        send_signal(self.data)


if __name__ == "__main__":
    HOST, PORT = "", 1100

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    logger.info('socket establecido')

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
