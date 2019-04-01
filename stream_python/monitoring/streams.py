import threading
from kafka import KafkaConsumer
import random as rd

map = {-1: 1}
kafkaServer = 'localhost:9092'
started = False


def init_consumer():
    try:
        consumer = KafkaConsumer('test',
                                 bootstrap_servers=kafkaServer)
        for msg in consumer:
            value = int.from_bytes(msg.value, byteorder='little')
            key = int.from_bytes(msg.key, byteorder='little')
            # print('{}:{}'.format(key, value))
            map[key] = value
    except:
        print('Kafka Server Not Found on {}'.format(kafkaServer))


def alterRandMap():
    map[-1] = rd.randint(0, 100)


def otherMain():
    if not started:
        threading.Thread(target=init_consumer, daemon=True).start()
    return map
