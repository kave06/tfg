import os

try:
    from app.model.rabbitMQ import connect_queue_receiver
    from app.model.relay_state import relay_state
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from model.rabbitMQ import connect_queue_receiver
    from model.relay_state import relay_state
    from modules.logger import create_log
    from modules.config import *

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/logs/producer'
logger = create_log(logger_name)


def main():
    relay_state()


if __name__ == '__main__':
    main()
