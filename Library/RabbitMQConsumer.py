import pika
from Library.GeneratePortfolio import *

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
        msg_decoded = body.decode("utf-8")
        msg = PGMessage.from_json(msg_decoded)
        if msg.PGMessageType == PGMessageType.Generate.value:
            GeneratePortfs()

    def startserver(self):
        self._channel.basic_consume(
            queue=self.queue,
            on_message_callback=rabbitMqConsumer.callback,
            auto_ack=True)
        self._channel.start_consuming()