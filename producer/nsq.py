import gnsq
import utils.utils as util
import mq
import producer


#参数opt 1.auth_secret 认证字符串
class NsqProducer:
    def __init__(self, addresss='localhost:4150',**opt):
        self.producer = gnsq.Producer(nsqd_tcp_addresses=addresss,max_backoff_duration=128,**opt)
        self.producer.start()

    #route: topic
    def Publish(self, msg, **route):
        self.producer.publish(route.get("topic"), msg.encode(encoding="utf-8"))


    def DelayPublish(self, delay, msg, **route):
        if util.Typeof(delay) != util.INT:
            raise Exception("delay error")
        self.producer.publish(route.get("topic"), msg.encode(encoding="utf-8"),defer=delay)


