import os

try:
    from app.model.rabbitMQ import start_consumer_ambient
    from app.modules.logger import create_log
except ImportError:
    from model.rabbitMQ import start_consumer_ambient
    from modules.logger import create_log

APP_DIR = os.getcwd()
logger_name = APP_DIR + '/logs/queues'
logger = create_log(logger_name)

# TODO change file in systemctl gui
if __name__ == '__main__':
    start_consumer_ambient()
