import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import numpy as np
import pandas as pd


print('test')
inputs = Input(shape=(31, ))
x = Dense(64, activation='sigmoid')(inputs)
x = Dense(64, activation='sigmoid')(x)
predictions = Dense(31, activation='softmax')(x)

model = Model(inputs=inputs, outputs=predictions)
model.compile(
    optimizer=tf.train.AdamOptimizer(0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy'])

orig = pd.read_csv('./data/datos.csv')
orig = orig.drop('Week', axis=1)
pdata = orig[1:]
data = pdata.values
labels = orig[0:-1]
labels = labels.values
# print(data)
# print(labels)

model.fit(data, labels, epochs=30, batch_size=32)
model.evaluate(data, labels, batch_size=32)
p = data[1]
# print(p)
result = model.predict(data)
