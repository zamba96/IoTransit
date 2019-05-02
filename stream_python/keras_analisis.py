import tensorflow as tf
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Input, Dense
from tensorflow.keras import layers
from tensorflow import keras
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt


# PostgreSQL connection
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

st = "SELECT * FROM lecturas"
cursor.execute(st)
records = cursor.fetchall()
df = pd.DataFrame(data=records)
df = df.drop(0, axis=1)
data = df.values
train_dataset = df.sample(frac=0.8, random_state=0)
test_dataset = df.drop(train_dataset.index)
train_stats = train_dataset.describe()
train_stats = train_stats.transpose()


def norm(x):
    return((x - train_stats['mean']) / train_stats['std'])


def deNorm(x):
    return(x * train_stats['std'] + train_stats['mean'])


normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)


def build_model():
    model = keras.Sequential([
        layers.Dense(64, activation=tf.nn.relu,
                     input_shape=[len(train_dataset.keys())]),
        layers.Dense(128, activation=tf.nn.relu),
        layers.Dense(64, activation=tf.nn.relu),
        layers.Dense(31)])

    optimizer = tf.train.AdamOptimizer(0.01)
    model.compile(loss='mean_squared_error',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    return model


model = build_model()
model.summary()

# inputs = Input(shape=(31, ))
# x = Dense(128, activation='sigmoid')(inputs)
# x = Dense(128, activation='sigmoid')(x)
# predictions = Dense(31, activation='softmax')(x)
#
# model = Model(inputs=inputs, outputs=predictions)
# model.compile(
#     optimizer=tf.train.AdamOptimizer(0.001),
#     loss='categorical_crossentropy',
#     metrics=['accuracy'])


# print(data)
# print(labels)

# model.fit(data, labels, epochs=30, batch_size=32)
# model.evaluate(data, labels, batch_size=32)
# p = data[1]
# print(p)

class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0:
            print('')
        print('.', end='')


train_labels = train_dataset.drop([train_dataset.index[0]])
test_labels = test_dataset.drop([test_dataset.index[0]])
train_labels = norm(train_labels)
train_dataset.drop(train_dataset.tail(1).index, inplace=True)
test_dataset.drop(test_dataset.tail(1).index, inplace=True)
normed_train_data.drop(normed_train_data.tail(1).index, inplace=True)


EPOCHS = 5000

history = model.fit(
    normed_train_data, train_labels,
    epochs=EPOCHS, validation_split=0.2, verbose=0,
    callbacks=[PrintDot()])

print("\n")
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print(hist.tail())

example_batch = normed_train_data[:1]
example_result = model.predict(example_batch)
example_result = pd.DataFrame(example_result)
print(train_dataset[:1])
print(deNorm(example_result))

cursor.close()
connection.close()


def plot_history(history):
    hist = pd.DataFrame(history)
    hist['epoch'] = history.epoch
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['mean_absolute_error'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
             label='Val Error')
    plt.ylim([0, 1])
    plt.legend()

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(hist['epoch'], hist['mean_squared_error'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_squared_error'],
             label='Val Error')
    plt.ylim([0, 2])
    plt.legend()
    plt.show()


plot_history(hist)
