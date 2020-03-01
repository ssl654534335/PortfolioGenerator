import pika
import ast

class rabbitMqConsumer():

    def __init__(self, queue, host):
        self.host = host
        self.queue = queue
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self._channel = self._connection.channel()
        self._tem = self._channel.queue_declare(queue=self.queue)
        print("Server started waiting for Messages ")

    @staticmethod
    def callback(ch,method, properties, body):
        msg = body.decode("utf-8")
        try:
            msg = ast.literal_eval(msg)
            print('decoded')
            print(type(msg))
            print("Data Received : {}".format(msg))
        except:
            print(type(msg))
            print("Data Received : {}".format(msg))

    def startserver(self):
        self._channel.basic_consume(
            queue=self.queue,
            on_message_callback=rabbitMqConsumer.callback,
            auto_ack=True)
        self._channel.start_consuming()


if __name__ == "__main__":
    server = rabbitMqConsumer('UserDB-PortfGen', "localhost")
    server.startserver()