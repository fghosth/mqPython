import gnsq
from multiprocessing import Process

class NsqConsumer:
    def __init__(self, host, auth=''):
        self._host = host
        self._auth = auth
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
            conn.close()

    def listen(self, receiver):
        consumer = gnsq.Consumer(receiver.topic, receiver.channel, self._host)
        @consumer.on_message.connect
        def handler(consumer, message):
            receiver.on_message_callback(message.body)
        consumer.start()

# consumer = gnsq.Consumer('111111ffffffff', 'channel', 'localhost:4150')
#
#
# @consumer.on_message.connect
# def handler(consumer, message):
#     print('got message:', message.body)
#
#
# consumer.start()
