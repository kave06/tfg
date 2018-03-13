import pika
import json
from datetime import datetime

try:
    from app.modules.logger import create_log
except ImportError:
    from modules.logger import create_log

logger = create_log('prototype')
USERNAME = 'xxxx'
PASSW = 'xxxx'
HOST = 'xxxxxxxxxxxxxxx'
PORT = 1234


def connect_queue():
    credentials = pika.PlainCredentials(username=USERNAME, password=PASSW)
    parameters = pika.ConnectionParameters(host=HOST, port=PORT,
                                           credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    return connection


def send_data_queue(connection, body):
    body['date'] = datetime.now()
    logger.info(body)
    channel = connection.channel()
    channel.queue_declare(queue='sensors_data')
    channel.basic_publish(exchange='', routing_key='sensors_data',
                          body=json.dumps(body, sort_keys=True, default=str))
    connection.close()

    logger.info(body)
