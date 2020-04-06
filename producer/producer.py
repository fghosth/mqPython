class Producer:
    def __init__(self):
        pass

    def Publish(self, msg, **route):
        raise NotImplementedError

    def DelayPublish(self, delay, msg, **route):
        raise NotImplementedError


class AgentProducer(Producer):

    def __init__(self, producer):
        self.send_obj = producer

    def Publish(self, msg, **route):
        self.send_obj.Publish(msg, **route)

    def DelayPublish(self, delay, msg, **route):
        self.send_obj.DelayPublish(delay, msg, **route)
