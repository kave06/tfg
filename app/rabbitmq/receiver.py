import pika


credentials = pika.PlainCredentials(username='kave', password='hola')
# parameters = pika.ConnectionParameters(host='89.128.192.144', port=1838,
#                                        virtual_host='/',
#                                        credentials=credentials)
parameters = pika.ConnectionParameters(credentials=credentials)
connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

channel.queue_declare(queue='sensors_data')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(callback,
                      queue='sensors_data',
                      no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
