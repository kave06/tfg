import pika
import json
from datetime import datetime
from pika import exceptions

try:
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from modules.logger import create_log
    from modules.config import *

logger = create_log('prototype')


def connect_queue() -> pika.BlockingConnection:
    connection = ''
    try:
        credentials = pika.PlainCredentials(username=rabbit_user, password=rabbit_pass)
        parameters = pika.ConnectionParameters(host=rabbit_host, port=rabbit_port,
                                               blocked_connection_timeout=300,
                                               heartbeat_interval=600,
                                               credentials=credentials)
        connection = pika.BlockingConnection(parameters=parameters)
        return connection
    except exceptions as err:
        # if connection.is_closed:
        logger.error(err)
        return connection


def send_queue_ambient(connection:pika.BlockingConnection,queue, body):
    try:
        body['date'] = datetime.now()
    except:
        one = 1
    logger.info(body)

    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='', routing_key=queue,
                              body=json.dumps(body, sort_keys=True, default=str))
        connection.close()
    except exceptions as err:
        logger.error(err)


def send_queue_relay(connection:pika.BlockingConnection, state):
    logger.info(state)

    try:
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_queue_relay_state)
        channel.basic_publish(exchange='', routing_key=rabbit_queue_relay_state,
                              body=json.dumps(state, default=str))
        connection.close()

    except exceptions as err:
        logger.error(err)
