import pika
import json

class MQclient(object):

    def __init__(self, config):
        self.config = config
        credentials = pika.PlainCredentials(
            username=self.config['mq_username'],
            password=self.config['mq_password'])

        parameters = pika.ConnectionParameters(
            host=self.config['mq_host'],
            virtual_host=self.config['mq_vhost'],
            credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)

    def get_channel(self, queue):
        channel = self.connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        return channel

    def close_connection(self):
        self.connection.close()

    def push(self, data, queue='access'):
        channel = self.connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        message = json.dumps(data)
        result = channel.basic_publish(exchange='',
                                       routing_key=queue,
                                       body=message,
                                       properties=pika.BasicProperties(
                                       delivery_mode=2))
        if result:
            print "(message %s added to queue %s', message, queue)"
