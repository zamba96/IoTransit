import threading
import time
# import matplotlib
from kafka import KafkaConsumer
from kafka import KafkaProducer
# import numpy as np
import tkinter as tk
import json

kafkaServer = 'localhost:9092'

map = {-1: 1}
top = tk.Tk()
labels = [[]]
vars = [[]]
try:
    producer = KafkaProducer(bootstrap_servers=kafkaServer)
except:
    print('Kafka Server Not Found on {}'.format(kafkaServer))


def main():
    n = 8
    for i in range(n):
        map[i] = -1
    threading.Thread(target=init_consumer, daemon=True).start()
    # print("test")
    while(True):
        # print(map)
        js = json.dumps(map)
        sendMain(js)
        time.sleep(2)


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


def sendMain(msg):
    print(msg)
    try:
        producer.send('liveData', key='timestamp',
                      value=msg)
        producer.flush()
    except:
        print('Kafka Server Not Found on {}'.format(kafkaServer))


def drawGUI():

    for k, v in map.items():
        sk = tk.StringVar(top)
        sv = tk.StringVar(top)
        sk.set('{}'.format(k))
        sv.set('{}'.format(v))
        varRow = [sk, sv]
        lk = tk.Label(top, text=sk)
        lv = tk.Label(top, text=sv)
        row = [lk, lv]
        labels.append(row)
        vars.append(varRow)
        print(vars)
    r = 0
    c = 0
    for row in labels:
        for col in row:
            col.grid(row=r, column=c)
            c += 1
            if c == 2:
                r += 1
                c = 0

    top.mainloop()


def refreshGUI():
    print("test")
    for row in labels:
        for col in row:
            col.set


if __name__ == '__main__':
    main()
