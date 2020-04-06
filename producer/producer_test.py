# import unittest
import nsq
import mq
import producer
import amqp
import utils.AliyunCredentialsProvider3 as credentials


# nsq发送测试
def NSQProudcerTest():
    nsp = nsq.NsqProducer(addresss='localhost:4150', auth_secret=3)
    mqp = producer.AgentProducer(nsp)
    mqp.DelayPublish(5000, "aaaaaa", topic="111111ffffffff")
    mqp.Publish("aaaaaa", topic="111111ffffffff")


NSQProudcerTest()


# rabbitmq 发送测试
def RabbitmqProducerTest():
    am = amqp.AMQPProducer(host='localhost', port=5672, virtual_host='/', user='guest', password='guest',
                           arguments={"x-delay": 45}, aaa=33)
    mqp = producer.AgentProducer(am)
    mqp.DelayPublish(10, "xxx", arguments={"x-delay": 45}, exchange="report.hexcloud", routing_key="mtask",exchange_type="fanout",)
    mqp.Publish("xxx", arguments={"x-delay": 45}, exchange="report.hexcloud",exchange_type="fanout", routing_key="mtask")

# RabbitmqProducerTest()


# ali amqp 发送测试
def AliAMQPProducerTest():
    ak = "LTAI4FqHC1FBWvsYEn68dXQK"
    sk = "6akk4wed4ZyMIR95voqGxZ17Z0z0w1"
    instanceId = "1551953348333975"  # // 请替换成您阿里云AMQP控制台首页instanceId
    cred = credentials.AliyunCredentialsProvider(access_key=ak, access_secret=sk, instanceId=instanceId)
    user = cred.get_username()
    pwd = cred.get_password()
    host = "1551953348333975.mq-amqp.cn-shanghai-a.aliyuncs.com"
    port = "5672"
    am = amqp.AMQPProducer(host=host, port=port, virtual_host='hex1', user=user, password=pwd,arguments={"x-delay": 45}, aaa=33)
    mqp = producer.AgentProducer(am)
    mqp.DelayPublish(1000, "xxx", exchange="hex_test", routing_key="task",exchange_type="direct")
    mqp.Publish("xxx",  exchange="hex_test", routing_key="task",exchange_type="direct")

# AliAMQPProducerTest()




# class NsqProducerTest(unittest.TestCase):
#     def setUp(self) -> None:
#         '''c的准备工作
#         :return:
#         '''
#         self.clac = nsq.NsqProducer({"aa":3})
#
#     def tearDown(self) -> None:
#         '''
#         测试之后的收尾
#         如关闭数据库
#         :return:
#         '''
#         pass
#     def test_Publish(self):
#         ret = self.clac.Publish((11, 22), {"aa": 2, "bb": "dd"})
#         self.assertEqual(ret, ((11, 22), {"aa": 2, "bb": "dd"}))
#
#     def test_DelayPublish(self):
#         ret = self.clac.DelayPublish(10, "22", "22")
#         self.assertEqual(ret, (10, '22', '22'))
#
#
# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(NsqProducerTest('test_Publish'))
#     suite.addTest(NsqProducerTest('test_DelayPublish'))
#
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
