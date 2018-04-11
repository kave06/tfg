import socketserver
import os

try:
    from app.modules.logger import create_log
    from app.modules.flags import Var
    from app.modules.config import *

except ImportError:
    from modules.logger import create_log
    from modules.flags import Var
    from modules.config import *

# APP_DIR = os.getcwd()
# logger_name = APP_DIR + '/app/logs/prototype'
# try:
#     logger = create_log(logger_name)
# except:
#     logger_name = APP_DIR + '/logs/prototype'
#     logger = create_log(logger_name)

# logger_name = '/home/kave/1tfg/prototipo/tfg/app/logs/prototype'
# logger = create_log(logger_name)

# try:
#     logger = create_log('app/logs/prototype')
# except:
#     logger = create_log('logs/prototype')

try:
    logger = create_log('app/logs/' + name_logger)
except:
    logger = create_log('logs/' + name_logger)


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
        # logger.debug(self.data)
        Var.STACK_STATE.append(self.data.decode())
        Var.RELAY_STATE = self.data.decode()
        # logger.debug('RELAY_STATE = {}'.format(Var.RELAY_STATE))

        # logger.info('{} send {}'.format(self.client_address[0], self.data.decode()))


def launch_socket_relay_state():
    HOST, PORT = "", webserver_socket_port_relay_state_in

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
