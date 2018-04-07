import pika
import json
from datetime import datetime
from pika import exceptions

try:
    from app.model.database import connect_db, send_data
    from app.modules.logger import create_log
    from app.modules.config import *
    from app.modules.flags import *
except ImportError:
    from model.database import connect_db, send_data
    from modules.logger import create_log
    from modules.config import *
    from modules.flags import *

logger = create_log('prototype')

STACK_STATE = []
RELAY_STATE = 'empty'


def connect_queue_sender() -> pika.BlockingConnection:
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
        Flag.rabbit_cnx_relay_state = False

    return connection


def connect_queue_receiver(queue, callback):
    credentials = pika.PlainCredentials(username=rabbit_user, password=rabbit_pass)
    parameters = pika.ConnectionParameters(credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback_relay_state,
                          queue=queue,
                          no_ack=True)
    return channel


# sender
def send_queue_ambient(connection: pika.BlockingConnection, body):
    body['date'] = datetime.now()
    # logger.info(body)

    try:
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_queue_ambient)
        channel.basic_publish(exchange='', routing_key=rabbit_queue_ambient,
                              body=json.dumps(body, sort_keys=True, default=str))
        connection.close()
    except Exception as err:
        logger.error(err)


def send_queue_relay(connection: pika.BlockingConnection, state):
    # logger.info(state)

    try:
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_queue_relay_state)
        channel.basic_publish(exchange='', routing_key=rabbit_queue_relay_state,
                              body=json.dumps(state, default=str))
        # connection.close()
        # logger.debug(state)

    except Exception as err:
        logger.error(err)


# receiver
def callback_ambient(ch, method, properties, body):
    ambient = json.loads(body.decode())

    logger.info('sensor: {}, date: {} temp: {}ºC, humi: {}%'
                .format(ambient['sensor'],
                        ambient['date'],
                        ambient['temperature'],
                        ambient['humidity']))

    cnx = connect_db()
    send_data(cnx, ambient)


def callback_relay_state(ch, method, properties, body):
    global RELAY_STATE
    state = json.loads(body.decode())
    RELAY_STATE = state
    STACK_STATE.append(state)
    # print(RELAY_STATE)
    # logger.info(state)
    # print('hola')
    # print(state)
    # logger.info(STACK_STATE)
    # print(STACK_STATE)


def start_consumer():
    channel_relay_state = connect_queue_receiver(rabbit_queue_relay_state, callback_relay_state)
    channel_relay_state.start_consuming()
