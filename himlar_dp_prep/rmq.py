import pika
import json
import pyramid.httpexceptions as exc

class MQclient(object):

    def __init__(self, config):
        self.config = config
	try:
            credentials = pika.PlainCredentials(
                username=self.config['mq_username'],
                password=self.config['mq_password'])
            parameters = pika.ConnectionParameters(
                host=self.config['mq_host'],
                virtual_host=self.config['mq_vhost'],
                credentials=credentials,
                connection_attempts=5,
                retry_delay=3,
                socket_timeout=10,
                blocked_connection_timeout=30)
            self.connection = pika.BlockingConnection(parameters)
        except:
            #raise ValueError('HTTP error occurred.')
	    raise exc.HTTPInternalServerError("HTTP error occurred.")

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
            print ('Message: %s', message, ' added to queue: ', queue)
	self.close_connection()
