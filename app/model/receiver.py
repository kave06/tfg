import pika
import json
import sys, os

# sys.path.append('../modules')
# sys.path.append('../model')

# print(sys.path)
# print('----------------------------------')
APP_DIR = os.path.dirname(os.path.realpath(__file__))
# print(APP_DIR)
path_modules = APP_DIR + '/../modules'
path_model = APP_DIR + '/../model'
sys.path.append(path_model)
sys.path.append(path_modules)
# print('----------------------------------')
# print(sys.path)

try:
    from app.model.database import connect_db, send_data
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from model.database import connect_db, send_data
    from modules.logger import create_log
    from modules.config import *

# APP_DIR = os.path.dirname(os.path.realpath(__file__))
# logger_name = APP_DIR + '/logs/prototype'
# logger = create_log(logger_name)

logger = create_log('prototype')

STACK_STATE = []

def connect_queue(queue, callback):
    credentials = pika.PlainCredentials(username=rabbit_user, password=rabbit_pass)
    parameters = pika.ConnectionParameters(credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_queue_ambient)
    channel.basic_consume(callback_ambient(),
                          queue=rabbit_queue_ambient,
                          no_ack=True)
    return channel


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
    state = json.loads(body.decode())
    print(state)
    STACK_STATE.append(state)
    print(STACK_STATE)




def main():
    channel_ambient = connect_queue(rabbit_queue_ambient, callback_ambient())
    # channel_relay_state = connect_queue(rabbit_queue_relay_state, callback_relay_state())
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel_ambient.start_consuming()
    # channel_relay_state.start_consuming()


if __name__ == '__main__':
    main()
