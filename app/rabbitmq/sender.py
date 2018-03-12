import pika

credentials = pika.PlainCredentials(username='kave', password='hola')
parameters = pika.ConnectionParameters(host='157.88.58.134', port=5578,
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)


channel = connection.channel()

channel.queue_declare(queue='sensors_data')

channel.basic_publish(exchange='',
                      routing_key='sensors_data',
                      body="{'humidity': '39.80', 'sensor': '2', 'temperature': '21.40'}")
                    # body='Hello World!')

print(" [x] Sent 'Hello World!'")
connection.close()