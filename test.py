import logging
import pika

# logging.basicConfig(level=logging.ERROR)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(
    "sss",
    passive=False,
    durable=True,
    exclusive=False,
    auto_delete=False,
    arguments={'x-expires':3000}
)
channel.exchange_declare(
    exchange="report.hexcloud",
    exchange_type="fanout",
    passive=False,
    durable=True,
    auto_delete=False)

print("Sending message to create a queue")
channel.basic_publish(
    'report.hexcloud', 'mtask', 'xxxxxxx',
    pika.BasicProperties(content_type='text/plain', delivery_mode=1))

# connection.sleep(5)
#
# print("Sending text message to group")
# channel.basic_publish(
#     'test_exchange', 'group_key', 'Message to group_key',
#     pika.BasicProperties(content_type='text/plain', delivery_mode=1))
#
# connection.sleep(5)
#
# print("Sending text message")
# channel.basic_publish(
#     'test_exchange', 'standard_key', 'Message to standard_key',
#     pika.BasicProperties(content_type='text/plain', delivery_mode=1))

connection.close()
