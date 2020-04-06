import pika
import utils.utils as util
import mq


class AMQPProducer:
    def __init__(self, host='localhost', port=5672, virtual_host='/', user='guest', password='guest', **exchangeArgs):
        self._credentials = pika.PlainCredentials(user, password)
        self._parameters = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host,
                                                     credentials=self._credentials)
        self._exchangeArgs = exchangeArgs

    def Publish(self, msg, **route):
        connection = pika.BlockingConnection(self._parameters)
        channel = connection.channel()
        channel.basic_publish(
            exchange=route.get("exchange"), routing_key=route.get("routing_key"), body=msg,
            properties=pika.BasicProperties(content_type='text/plain', delivery_mode=1))
        connection.close()

    def DelayPublish(self, delay, msg, **route):
        if util.Typeof(delay) != util.INT:
            raise Exception("delay error")
        connection = pika.BlockingConnection(self._parameters)
        channel = connection.channel()

        if util.Typeof(route.get("arguments")) != util.DICT:
            args = {**{mq.Expires: 3000}, **{mq.Delay: delay}}
        else:
            args = {**{mq.Expires: 3000}, **{mq.Delay: delay}, **route.get("arguments")}
        channel.queue_declare(
            "delay" + str(delay),
            passive=route.get("passive", False),
            durable=route.get("durable", True),
            exclusive=route.get("exclusive", False),
            auto_delete=route.get("auto_delete", False),
            arguments=args
        )
        channel.exchange_declare(
            exchange=route.get("exchange"),
            exchange_type=route.get("exchange_type"),
            passive=route.get("passive",False),
            durable=route.get("durable",True),
            auto_delete=route.get("auto_delete",False),
            arguments=self._exchangeArgs
        )
        channel.basic_publish(
            exchange=route.get("exchange"), routing_key=route.get("routing_key"), body=msg,
            properties=pika.BasicProperties(content_type='text/plain', delivery_mode=1))
        connection.close()
