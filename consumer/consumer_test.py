import amqp
import consumer
import utils.AliyunCredentialsProvider3 as credentials
import utils.utils as util
import mq
import time
from multiprocessing import Process
import nsqC

class NsqReceiver:
    topic=""
    channel=""
    def __init__(self,topic,channel):
        self.topic = topic
        self.channel = channel
        # 返回True 则ack消息

    def on_message_callback(self, body):
        print(body)
        return True

    def on_error(self, err):
        print(err)


def NsqConsumerTest():
    reciver1 = NsqReceiver(topic="111111ffffffff",channel="test")
    reciver2 = NsqReceiver(topic="payflow_Cancle",channel="test")
    nsqc = nsqC.NsqConsumer("localhost:4150")
    agentC = consumer.AgentConsumer(nsqc)
    agentC.RegisterReceiver(reciver1)
    agentC.RegisterReceiver(reciver2)
    agentC.Start()

NsqConsumerTest()


class RabbitReceiver1:
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
                 arguments=None,
                 ):
        self.queue_name = queue_name
        self.route_key = route_key
        self.passive = passive
        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        if util.Typeof(arguments)==util.DICT:
            self.arguments = {**self.arguments, **arguments}

    # 返回True 则ack消息
    def on_message_callback(self, body):
        print(body)
        return True

    def on_error(self, err):
        print(err)


def RabbitMqConsumerTest():
    reciver1 = RabbitReceiver1("reportstask", "mtask")
    reciver2 = RabbitReceiver1("report2", "mtask")
    rc1 = amqp.AMQPConsumer(host='localhost', port=5672, virtual_host='/', user='guest', password='guest',
                            arguments={"x-delay": 3000}, exchange="report.hexcloud", exchange_type="fanout")
    agentC = consumer.AgentConsumer(rc1)
    agentC.RegisterReceiver(reciver1)
    agentC.RegisterReceiver(reciver2)
    agentC.Start()
# RabbitMqConsumerTest()


def AliAMQPConsumerTest():
    reciver1 = RabbitReceiver1("reportstask", "mtask",arguments={mq.DeadLetterExchange:"hexDead",mq.DeadLetterRoutingKey:"report"})
    reciver2 = RabbitReceiver1("report1", "task")
    ak = "x"
    sk = "x"
    instanceId = "x"  # // 请替换成您阿里云AMQP控制台首页instanceId
    cred = credentials.AliyunCredentialsProvider(access_key=ak, access_secret=sk, instanceId=instanceId)
    user = cred.get_username()
    pwd = cred.get_password()
    host = "1551953348333975.mq-amqp.cn-shanghai-a.aliyuncs.com"
    port = "5672"
    rc1 = amqp.AMQPConsumer(host=host, port=port, virtual_host='hex1', user=user, password=pwd,
                            arguments={"DeadLetterExchange": "hexDead","DeadLetterRoutingKey":"report"}, exchange="hex_test", exchange_type="direct")
    agentC = consumer.AgentConsumer(rc1)
    agentC.RegisterReceiver(reciver1)
    agentC.RegisterReceiver(reciver2)

    def a():
        time.sleep(5)
        agentC.Stop()

    try:
        p1 = Process(target=a)
        p2 = Process(target=agentC.Start)
        p2.start()
        time.sleep(3)
        print(agentC.consumer_obj._connection)
        p1.start()
    except:
        print("Error: unable to start thread")

# AliAMQPConsumerTest()
