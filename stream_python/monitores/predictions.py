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
                             bootstrap_servers=kafkaServer,
                             value_deserializer=lambda v:
                             json.loads(v).encode('utf-8'))
    print("[INFO] Consumer OK")
except:
    print('Cosumer: Kafka Server Not Found on {}'.format(kafkaServer))
    exit()

# Main loop
print('[INFO] livePred channel monitor')
for msg in consumer:
    map = {}
    a = json.loads(msg.value)
    # print(a)

    for (x, y) in a.items():
        map[x] = y
    print(map)
