import os

try:
    from app.model.rabbitMQ import connect_queue_receiver
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from model.rabbitMQ import connect_queue_receiver
    from modules.logger import create_log
    from modules.config import *

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/logs/queues'
logger = create_log(logger_name)

# TODO change file in systemctl gui

def main():
    channel_ambient = connect_queue_receiver(rabbit_queue_ambient, rabbit_callback_ambient)
    channel_relay_state = connect_queue_receiver(rabbit_queue_relay_state, rabbit_callback_relay_state)
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel_ambient.start_consuming()
    channel_relay_state.start_consuming()


if __name__ == '__main__':
    main()
