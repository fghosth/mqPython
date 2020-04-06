class Consumer:
    def __init__(self):
        pass

    def RegisterReceiver(self, Receiver):
        raise NotImplementedError

    def Start(self):
        raise NotImplementedError

    def Stop(self):
        raise NotImplementedError


class AgentConsumer(Consumer):

    def __init__(self, consumer):
        self.consumer_obj = consumer

    def RegisterReceiver(self, Receiver):
        self.consumer_obj.RegisterReceiver(Receiver)

    def Start(self):
        self.consumer_obj.Start()

    def Stop(self):
        self.consumer_obj.Stop()


class Receiver:
    queue_name = ""
    route_key = ""
    passive = False
    durable = True
    exclusive = False
    auto_delete = False
    arguments = {}

    def __init__(self, queue_name,
                 route_key,
                 passive=False,
                 durable=True,
                 exclusive=False,
                 auto_delete=False,
                 **arguments,
                 ):
        self.queue_name = queue_name
        self.route_key = route_key
        self.passive = passive
        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        self.arguments = {**self.arguments, **arguments}

    # 返回True 则ack消息
    def on_message_callback(self,body):
        raise NotImplementedError

    def on_error(self):
        raise NotImplementedError
