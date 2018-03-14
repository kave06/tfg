import pika
import json
from datetime import datetime

try:
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from modules.logger import create_log
    from modules.config import *

logger = create_log('prototype')


def connect_queue():
    connection = ''
    try:
        credentials = pika.PlainCredentials(username=rabbit_user, password=rabbit_pass)
        parameters = pika.ConnectionParameters(host=rabbit_host, port=rabbit_port,
                                               blocked_connection_timeout=300,
                                               heartbeat_interval=600,
                                               credentials=credentials)
        connection = pika.BlockingConnection(parameters=parameters)
        return connection
    except Exception as err:
        # if connection.is_closed:
        logger.error(err)
        return connection


def send_data_queue(connection, body):

    body['date'] = datetime.now()
    logger.info(body)

    try:
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_queue)
        channel.basic_publish(exchange='', routing_key=rabbit_queue,
                              body=json.dumps(body, sort_keys=True, default=str))
        connection.close()
    except Exception as err:
        logger.error(err)

