import pika
import json

try:
    from app.model.database import connect_db, send_data
    from app.modules.logger import create_log
except ImportError:
    from model.database import connect_db, send_data
    from modules.logger import create_log

QUEUE = 'sensors_data'

logger = create_log('prototype')

def connect_queue():

    credentials = pika.PlainCredentials(username='kave', password='hola')
    parameters = pika.ConnectionParameters(credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    channel.basic_consume(callback,
                          queue=QUEUE,
                          no_ack=True)
    return channel



def callback(ch, method, properties, body):
    # print(" [x] Received %r" % body)
    print(" [x] Received %r" % json.loads(body.decode()))
    ambient = json.loads(body.decode())
    print(type(ambient))
    cnx = connect_db()
    send_data(cnx,ambient)


def main():

    channel = connect_queue()
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
