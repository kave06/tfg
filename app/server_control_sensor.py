import os

try:
    from app.model.receiver import connect_queue
    from app.modules.logger import create_log
except ImportError:
    from model.receiver import connect_queue
    from modules.logger import create_log

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/logs/prototype'
logger = create_log(logger_name)


def main():
    channel = connect_queue()
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
