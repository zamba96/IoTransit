from kafka import KafkaProducer
import random as rd
import time
import json


def kafkaServer():
    with open('config/ip.json') as json_file:
        data = json.load(json_file)
        print(data['ip'])
        return data['ip']


kafkaServer = kafkaServer()

try:
    producer = KafkaProducer(bootstrap_servers=kafkaServer)
except:
    print("Kafka Server Not Found")

id = 0
while(True):
    rand = rd.randint(1, 9999)
    producer.send('input', key=id.to_bytes(4, byteorder='little'),
                  value=rand.to_bytes(4, byteorder='little'))
    producer.flush()
    print('{}:{}'.format(id, rand))
    time.sleep(1 / 8)
    id += 1
    if id == 31:
        id = 0
