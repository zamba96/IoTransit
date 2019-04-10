import pandas as pd
from kafka import KafkaProducer
import time

try:
    producer = KafkaProducer(bootstrap_servers='34.210.181.142:9092')
except:
    print("Kafka Server Not Found")

data = pd.read_csv('./data/datos.csv')
data = data.drop('Week', axis=1)
data = data.values
while(True):
    for row in data:
        id = 0
        for cell in row:
            # print("{}:{}".format(id, cell))
            producer.send('input', key=id.to_bytes(4, byteorder='little'),
                          value=cell.item().to_bytes(4, byteorder='little'))
            id += 1
            time.sleep(0.005)
