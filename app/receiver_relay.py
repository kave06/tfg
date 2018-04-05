import pika
import json
import sys, os

APP_DIR = os.path.dirname(os.path.realpath(__file__))
path_modules = APP_DIR + '/../modules'
path_model = APP_DIR + '/../model'
sys.path.append(path_model)
sys.path.append(path_modules)

try:
    # from app.model.database import connect_db, send_data
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    # from model.database import connect_db, send_data
    from modules.logger import create_log
    from modules.config import *

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/logs/receiver_relay'
logger = create_log(logger_name)

# logger_name = APP_DIR + '/logs/queues'
# logger = create_log('queues')

STACK_STATE = []
RELAY_STATE = 'empty'


def connect_queue(queue, callback):
    credentials = pika.PlainCredentials(username=rabbit_user, password=rabbit_pass)
    parameters = pika.ConnectionParameters(credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=True)
    return channel


# def callback_ambient(ch, method, properties, body):
#     ambient = json.loads(body.decode())
#
#     logger.info('sensor: {}, date: {} temp: {}ºC, humi: {}%'
#                 .format(ambient['sensor'],
#                         ambient['date'],
#                         ambient['temperature'],
#                         ambient['humidity']))
#
#     cnx = connect_db()
#     send_data(cnx, ambient)


def callback_relay_state(ch, method, properties, body):
    state = json.loads(body.decode())
    RELAY_STATE = state
    # logger.info(state)
    # logger.debug('-------------------------------------------------------------')
    # print('hola')
    # print(state)
    # STACK_STATE.append(state)
    # logger.info(STACK_STATE)
    # print(STACK_STATE)



def main():
#     channel_ambient = connect_queue(rabbit_queue_ambient, callback_ambient())
    print('channel')
    channel_relay_state = connect_queue(rabbit_queue_relay_state, callback_relay_state)
#     # print(' [*] Waiting for messages. To exit press CTRL+C')
#     channel_ambient.start_consuming()
    print('start consuming')
    channel_relay_state.start_consuming()


if __name__ == '__main__':
    main()
