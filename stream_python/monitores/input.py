from kafka import KafkaConsumer
import json


def kafkaServer():
    with open('config/ip.json') as json_file:
        data = json.load(json_file)
        print(data['ip'])
        return data['ip']


kafkaServer = kafkaServer()

try:
    consumer = KafkaConsumer('livePred',
                             bootstrap_servers=kafkaServer)
    print("[INFO] Consumer OK")
except:
    print('Cosumer: Kafka Server Not Found on {}'.format(kafkaServer))
    exit()

# Main loop
for msg in consumer:
    value = int.from_bytes(msg.value, byteorder='little')
    key = int.from_bytes(msg.key, byteorder='little')
    print('{}:{}'.format(key, value))
