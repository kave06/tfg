import os

try:
    from app.model.rabbitMQ import start_consumer_ambient
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from model.rabbitMQ import start_consumer_ambient
    from modules.logger import create_log
    from modules.config import *

# logger = create_log(logger_name)

# logger_name = '/home/kave/1tfg/prototipo/tfg/app/logs/prototype'
# logger = create_log(logger_name)

# APP_DIR = os.getcwd()
# logger_name = APP_DIR + '/logs/' + name_logger
# print('--------------------------------------------------------------')
# print(logger_name)
# logger = create_log(logger_name )
# APP_DIR = os.getcwd()
# name = APP_DIR + '/logs/' + name_logger
# logger = create_log(name)

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)
if __name__ == '__main__':
    start_consumer_ambient()
