import threading
import time
# import matplotlib
from kafka import KafkaConsumer
import numpy as np

map = {-1: 1}


def main():
    n = 8
    for i in range(n):
        map[i] = -1
    # threading.Thread(target=init_consumer, daemon=True).start()
    init_consumer()


def init_consumer():
    consumer = KafkaConsumer('test',
                             bootstrap_servers='localhost:9092')
    for msg in consumer:
        value = int.from_bytes(msg.value, byteorder='little')
        key = int.from_bytes(msg.key, byteorder='little')
        # print('{}:{}'.format(key, value))
        map[key] = value


def init_consumer2():
    n = 8
    map2 = {-1: -1}
    consumer = KafkaConsumer('test',
                             bootstrap_servers='localhost:9092')
    for msg in consumer:
        value = int.from_bytes(msg.value, byteorder='little')
        key = int.from_bytes(msg.key, byteorder='little')
        # print('{}:{}'.format(key, value))
        map2[key] = value


def otherMain():

    threading.Thread(target=init_consumer, daemon=True).start()
    time.sleep(2)
    return map
