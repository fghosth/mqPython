import pika
from multiprocessing import Process


class AMQPConsumer:
    def __init__(self, host='localhost', port=5672, virtual_host='/', user='guest', password='guest', **exchange):
        self._credentials = pika.PlainCredentials(user, password)
        self._parameters = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host,
                                                     credentials=self._credentials)
        self._exchange = exchange
        self._receiver = []
        self._connection = []

    def RegisterReceiver(self, receiver):
        self._receiver.append(receiver)

    def Start(self):
        for receive in self._receiver:
            try:
                p1 = Process(target=self.listen, args=(receive,))
                p1.start()
            except:
                print("Error: unable to start thread")
            # self.listen(receive)

    def Stop(self):
        #TODO self._connection 为空不知道为什么
        for conn in self._connection:
            conn.channel().stop_consuming()
            conn.close()

    def listen(self, receiver):
        def _on_message_callback(chan, method_frame, header_frame, body, userdata=None):
            res = receiver.on_message_callback(body)
            if res == True:
                chan.basic_ack(delivery_tag=method_frame.delivery_tag)

        while (True):  # 意外断开,退出重连
            try:
                connection = pika.BlockingConnection(self._parameters)
                self._connection.append(connection)
                channel = connection.channel()
                channel.exchange_declare(
                    exchange=self._exchange.get("exchange"),
                    exchange_type=self._exchange.get("exchange_type"),
                    passive=self._exchange.get("passive", False),
                    durable=self._exchange.get("durable", True),
                    auto_delete=self._exchange.get("auto_delete", False),
                    arguments=self._exchange.get("arguments")
                )
                channel.queue_declare(
                    receiver.queue_name,
                    passive=receiver.passive,
                    durable=receiver.durable,
                    exclusive=receiver.exclusive,
                    auto_delete=receiver.auto_delete,
                    arguments=receiver.arguments
                )
                channel.queue_bind(
                    receiver.queue_name,
                    self._exchange.get("exchange"),
                    routing_key=receiver.route_key,
                    arguments=receiver.arguments
                )
                # channel.basic_qos(prefetch_count=1)
                channel.basic_consume(receiver.queue_name, _on_message_callback)
                channel.start_consuming()
            except pika.exceptions.ConnectionClosedByBroker as err:
                receiver.on_error(err)
                continue
            except pika.exceptions.AMQPChannelError as err:
                print("Caught a channel error: {}, stopping...".format(err))
                receiver.on_error(err)
                break
                # Recover on all other connection errors
            except pika.exceptions.AMQPConnectionError as err:
                print("Connection was closed, retrying...")
                receiver.on_error(err)
                continue
            except KeyboardInterrupt:
                print("KeyboardInterrupt, stoped")
                break

# def _on_message_callback(self,chan, method_frame, header_frame, body, userdata=None):
