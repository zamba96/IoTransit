import pandas as pd
import tensorflow as tf
from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
from tensorflow.keras import layers
from tensorflow import keras
import time
import argparse
import psycopg2


connection = None
cursor = None
try:
    connection = psycopg2.connect(user="postgres",
                                  password="12345",
                                  host="34.210.181.142",
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


def saveRecord(record, ts):
    st = "INSERT INTO pred VALUES (\n{}".format(ts)
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


parser = argparse.ArgumentParser(description='Arg Parser')
parser.add_argument(
    'modelPath',
    help='ruta al modelo Keras, si no se encuentra, se crea uno nuevo',
    default='no')


def kafkaServer():
    with open('config/ip.json') as json_file:
        data = json.load(json_file)
        print(data['ip'])
        return data['ip']


kafkaServer = kafkaServer()
print(kafkaServer)

producer = None
try:
    producer = KafkaProducer(bootstrap_servers=kafkaServer,
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))
    print("[INFO] Producer OK")
except:
    print('Producer: Kafka Server Not Found on {}'.format(kafkaServer))
    exit()

consumer = None

lastMap = {}
map = {}


numSensores = 31


def predict():
    batch = pd.DataFrame.from_dict(map, orient='index')
    batch = batch.transpose()
    try:
        batch = batch.drop(columns='-1')
    except:
        print('.')
    # print(batch)
    result = model.predict(batch)
    # print(result)
    return result


def createModel():
    global model
    model = keras.Sequential([
        layers.Dense(128, activation=tf.nn.relu,
                     input_shape=[numSensores]),
        layers.Dense(128, activation=tf.nn.relu),
        layers.Dense(128, activation=tf.nn.relu),
        layers.Dense(numSensores)])

    optimizer = tf.train.AdamOptimizer(0.01)
    model.compile(loss='mean_squared_error',
                  optimizer=optimizer,
                  metrics=['mse'])
    return model


def miniTrain():
    train = pd.DataFrame.from_dict(lastMap, orient='index')
    train = train.transpose()
    try:
        train = train.drop(columns='-1')
    except:
        print('.')

    label = pd.DataFrame.from_dict(lastMap, orient='index')
    label = label.transpose()
    try:
        label = label.drop(columns='-1')
    except:
        print('')

    model.fit(
        train, label,
        epochs=1,
        batch_size=1,
        verbose=1)


args = parser.parse_args()
modelPath = args.modelPath
# print(args.modelPath)
if args.modelPath == 'no':
    print('[INFO] Keras model not specified, creating new model')
    model = createModel()
    modelPath = 'keras_models/test.h5'
else:
    print('[INFO] Loading Keras model from {}'.format(
        args.modelPath))
    model = keras.models.load_model(args.modelPath)
    optimizer = tf.train.AdamOptimizer(0.01)
    model.compile(loss='mean_squared_error',
                  optimizer=optimizer,
                  metrics=['mse'])
model.summary()


def saveModel():
    model.save(modelPath)
    print('[INFO] Saved model to {}'.format(modelPath))


def sendPred(jsonParam):
    # print(jsonParam)
    id = int(time.time())
    producer.send('livePred', key=id.to_bytes(4, byteorder='little'),
                  value=jsonParam)
    producer.flush()


try:
    consumer = KafkaConsumer('liveData',
                             bootstrap_servers=kafkaServer,
                             value_deserializer=lambda v:
                             json.loads(v).encode('utf-8'))
    print("[INFO] Consumer OK")
except:
    print('Cosumer: Kafka Server Not Found on {}'.format(kafkaServer))
    exit()

# Main loop
timesTrained = 0
print('[INFO] IoTransit NN Predictor')
for msg in consumer:
    a = json.loads(msg.value)
    # print(a)
    lastMap = map
    map.clear()
    for (x, y) in a.items():
        map[x] = y
    prediction = predict()
    d_pred = {}
    i = 0
    for p in prediction[0]:
        d_pred[i] = float(p)
        # d_pred[i] = int(p)
        i += 1
    # print(d_pred)
    jsonMsg = json.dumps(d_pred)
    sendPred(jsonMsg)
    id = int(time.time())
    saveRecord(d_pred, id)
    miniTrain()
    timesTrained += 1
    if timesTrained % 50 == 0:
        saveModel()

    # ts = int.from_bytes(msg.key, byteorder='little')
    # print(ts)
    # map['timestamp'] = ts
