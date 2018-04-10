import socketserver
from serial import Serial
import os

try:
    from app.modules.logger import create_log
    from app.model.nano import send_signal
    from app.modules.flags import Var

except ImportError:
    from modules.logger import create_log
    from model.nano import send_signal

# APP_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.getcwd()
logger_name = APP_DIR + '/logs/prototype'
print(logger_name)
logger = create_log(logger_name)

# SERIAL_PORT = '/dev/ttyUSB0'
# BD = 9600


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request.sendall(self.data)

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        logger.debug(self.data)
        Var.STACK_STATE.append(self.data)
        Var.RELAY_STATE = self.data
        logger.debug('RELAY_STATE = {}'.format(Var.RELAY_STATE))

        # logger.info('{} send {}'.format(self.client_address[0], self.data.decode()))


if __name__ == "__main__":
    HOST, PORT = "", 1101

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # logger.info('Listening...')

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
