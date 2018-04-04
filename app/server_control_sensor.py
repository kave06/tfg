import os

try:
    from app.model.receiver import connect_queue, callback_ambient, callback_relay_state
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from model.receiver import connect_queue, callback_ambient, callback_relay_state
    from modules.logger import create_log
    from modules.config import *

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/logs/queues'
logger = create_log(logger_name)


def main():
    channel = connect_queue(rabbit_queue_ambient,callback_ambient())
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
