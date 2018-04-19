try:
    from app.model.rabbitMQ import start_consumer_ambient
    # from app.tools.logger import create_log
    # from app.tools.config import *
except ImportError:
    from model.rabbitMQ import start_consumer_ambient
    # from tools.logger import create_log
    # from tools.config import *

# try:
#     logger = create_log(webserver_logger)
# except:
#     logger = create_log(raspi_logger)
if __name__ == '__main__':
    start_consumer_ambient()
