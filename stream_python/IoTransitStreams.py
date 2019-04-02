import threading
import time
# import matplotlib
from kafka import KafkaConsumer
from kafka import KafkaProducer
# import numpy as np
import tkinter as tk
import json
import psycopg2

# PostgreSQL connection
connection = None
cursor = None
try:
    connection = psycopg2.connect(user="zamba",
                                  password="",
                                  host="localhost",
                                  port="5432",
                                  database="iotransit")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

kafkaServer = '54.149.247.97:9092'

map = {-1: 1}
top = tk.Tk()
labels = [[]]
vars = [[]]
try:
    producer = KafkaProducer(bootstrap_servers=kafkaServer,
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))
except:
    print('Producer: Kafka Server Not Found on {}'.format(kafkaServer))


def main():
    n = 31
    for i in range(n):
        map[i] = -1
    threading.Thread(target=init_consumer, daemon=True).start()
    # print("test")
    while(True):
        # print(map)
        js = json.dumps(map)
        id = sendMain(js)
        saveRecord(map, id)
        time.sleep(1)


def init_consumer():
    try:
        consumer = KafkaConsumer('input',
                                 bootstrap_servers=kafkaServer)
        for msg in consumer:
            value = int.from_bytes(msg.value, byteorder='little')
            key = int.from_bytes(msg.key, byteorder='little')
            # print('{}:{}'.format(key, value))
            map[key] = value
    except:
        print('Cosumer: Kafka Server Not Found on {}'.format(kafkaServer))


def sendMain(msg):
    # print(msg)
    id = int(time.time())
    producer.send('liveData', key=id.to_bytes(4, byteorder='little'),
                  value=msg)
    producer.flush()
    return id
    # print('SendMain: Kafka Server Not Found on {}'.format(kafkaServer))


def saveRecord(record, ts):
    st = "INSERT INTO lecturas VALUES (\n{}".format(ts)
    flag = True
    for k, v in record.items():
        if k != -1 and v != -1:
            st += ",\n{}".format(v)
        if v == -1:
            flag = False
    st += ");"
    # print(st)
    if flag:
        cursor.execute(st)
        connection.commit()


if __name__ == '__main__':
    main()
