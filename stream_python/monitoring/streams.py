import threading
from kafka import KafkaConsumer
import random as rd
import json

map = {}


def kafkaServer():
    with open('config/ip.json') as json_file:
        data = json.load(json_file)
        print(data['ip'])
        return data['ip']


kafkaServer = kafkaServer()


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


def init_consumer2():
    try:
        consumer = KafkaConsumer('liveData',
                                 bootstrap_servers=kafkaServer,
                                 value_deserializer=lambda v:
                                 json.loads(v).encode('utf-8'))
        for msg in consumer:
            a = json.loads(msg.value)
            # print(a)
            map.clear()
            for (x, y) in a.items():
                map[x] = y
            ts = int.from_bytes(msg.key, byteorder='little')
            # print(ts)
            map['timestamp'] = ts
    except:
        print('Kafka Server Not Found on {}'.format(kafkaServer))


def alterRandMap():
    map[-1] = rd.randint(0, 100)


def otherMain():
    global started
    if started is False:
        started = True
        # threading.Thread(target=init_consumer, daemon=True).start()
        threading.Thread(target=init_consumer2, daemon=True).start()

    return map
