import pika
import json

try:
    from app.model.database import connect_db, send_data
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from model.database import connect_db, send_data
    from modules.logger import create_log
    from modules.config import *

logger = create_log('prototype')


def connect_queue():
    credentials = pika.PlainCredentials(username=rabbit_user, password=rabbit_pass)
    parameters = pika.ConnectionParameters(credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_queue)
    channel.basic_consume(callback,
                          queue=rabbit_queue,
                          no_ack=True)
    return channel


def callback(ch, method, properties, body):
    ambient = json.loads(body.decode())
    cnx = connect_db()
    # logger.info(ambient)
    logger.info('sensor: {}, date: {} temp: {}ºC, humi: {}%'
                .format(ambient['sensor'],
                        ambient['date'],
                        ambient['temperature'],
                        ambient['humidity']))
    send_data(cnx, ambient)


def main():
    channel = connect_queue()
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
