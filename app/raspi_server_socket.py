import socketserver
from serial import Serial
import os

try:
    from app.modules.logger import create_log
    from app.model.nano import send_signal
except ImportError:
    from modules.logger import create_log
    from model.nano import send_signal

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/logs/socket'
logger = create_log(logger_name)

SERIAL_PORT = '/dev/ttyUSB0'
BD = 9600


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Escucha la señal que se le manda para encender y apagar el LED.

    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request.sendall(self.data)

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # logger.info(self.data)

        logger.info('{} send {}'.format(self.client_address[0], self.data.decode()))
        # print("{} wrote:".format(self.client_address[0]))
        # print(self.data)

        send_signal(self.data)


if __name__ == "__main__":
    HOST, PORT = "", 1100

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    # logger.info('Socket is open')

    arduino = Serial(SERIAL_PORT, BD)
    logger.info('Listening...')

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
