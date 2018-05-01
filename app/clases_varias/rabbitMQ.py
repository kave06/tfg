import os
import pika
import json
from datetime import datetime
import pika

try:
    from app.tools.config import *
    from app.clases_varias.connection import *
    from app.clases_varias.element import *
except ImportError:
    from tools.config import *
    from clases_varias.connection import *
    from clases_varias.element import *




class RabbitMQ(Connection):

    def __init__(self, username=rabbit_user, password=rabbit_pass,
                 host=rabbit_host, port=rabbit_port, timeout=300,
                 heartbeat_intervals=600):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.timeout = timeout
        self.heartbeat_interval = heartbeat_intervals
        self.connection = False
        self.channel = False


class Sender(RabbitMQ):

    def connected(self):
        'Connect to the queue'
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port,
                                               blocked_connection_timeout=self.timeout,
                                               heartbeat_interval=self.heartbeat_interval,
                                               credentials=credentials)
        try:
            self.connection = pika.BlockingConnection(parameters=parameters)
        except Exception as err:
            logger.error(err)

    def send(self, body: Ambient):
        ambient = dict(sensor=body.sensor, date=body.date,
                       temperature=body.temperature, humidity=body.humidity)

        try:
            channel = self.connection.channel()
            self.channel = self.connection.channel()
            channel.queue_declare(queue=rabbit_queue_ambient)
            channel.basic_publish(exchange='', routing_key=rabbit_queue_ambient,
                                  body=json.dumps(ambient, sort_keys=True, default=str))
            # connection.close()
        except Exception as err:
            logger.error(err)




class Receiver(RabbitMQ):
    def sapo(self):
        pass
    pass


try:
    from app.model.database import connect_db, send_data
    from app.tools.logger import create_log
    from app.tools.config import *
    from app.tools.flags import *
    from app.clases_varias.element import Ambient, Ambient
    # from app.tools.manage_file import write_file
except ImportError:
    from model.database import connect_db, send_data
    from tools.logger import create_log
    from tools.config import *
    from tools.flags import *
    from clases_varias.element import Ambient
    # from tools.manage_file import write_file

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


# TODO if server fail keep data in the queue
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

    return connection


def connect_queue_receiver(queue, callback):
    credentials = pika.PlainCredentials(username=rabbit_user, password=rabbit_pass)
    parameters = pika.ConnectionParameters(credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=True)
    return channel


# sender
def send_queue_ambient(connection: pika.BlockingConnection, body: Ambient):
    # body['date'] = datetime.now()
    # logger.info(body)

    # ambient = []
    ambient = dict(sensor=body.sensor, date=body.date,
                   temperature=body.temperature, humidity=body.humidity)

    try:
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_queue_ambient)
        channel.basic_publish(exchange='', routing_key=rabbit_queue_ambient,
                              body=json.dumps(ambient, sort_keys=True, default=str))
        # connection.close()
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
        Flag.rabbit_cnx_relay_state = False


# receiver
def callback_ambient(ch, method, properties, body):
    path = os.getcwd()
    file = path + '/logs/ambient'

    ambient = json.loads(body.decode())

    logger.info('sensor: {}, date: {} temp: {}ºC, humi: {}%'
                .format(ambient['sensor'],
                        ambient['date'],
                        ambient['temperature'],
                        ambient['humidity']))

    cnx = connect_db()
    send_data(cnx, ambient)
    # write_file(file, '{} {}'.format(datetime.now(),ambient))


# receiver
def callback_relay_state(ch, method, properties, body):
    path = os.getcwd()
    file = path + '/app/logs/relay_state'

    state = json.loads(body.decode())
    Var.RELAY_STATE = state
    Var.STACK_STATE.append(state)
    # write_file(file, '{} {}'.format(datetime.now(),state))


def start_consumer_ambient():
    channel_ambient = connect_queue_receiver(rabbit_queue_ambient, callback_ambient)
    channel_ambient.start_consuming()


def start_consumer_realy_state():
    channel_relay_state = connect_queue_receiver(rabbit_queue_relay_state, callback_relay_state)
    channel_relay_state.start_consuming()
