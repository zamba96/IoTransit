from kafka import KafkaProducer
import random as rd
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

id = 0
while(True):
    rand = rd.randint(1, 9999)
    producer.send('test', key=id.to_bytes(4, byteorder='little'),
                  value=rand.to_bytes(4, byteorder='little'))
    producer.flush()
    print('{}:{}'.format(id, rand))
    time.sleep(1 / 8)
    id += 1
    if id == 8:
        id = 0
