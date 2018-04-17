try:
    from app.model.rabbitMQ import start_consumer_ambient
    # from app.modules.logger import create_log
    # from app.modules.config import *
except ImportError:
    from model.rabbitMQ import start_consumer_ambient
    # from modules.logger import create_log
    # from modules.config import *

# try:
#     logger = create_log(webserver_logger)
# except:
#     logger = create_log(raspi_logger)
# TODO change name of file database_server_consumer.py
if __name__ == '__main__':
    start_consumer_ambient()
