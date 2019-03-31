import threading
import time
from kafka import KafkaConsumer
import numpy as np

map = np.zeros((1, 3))
print(map)
map.append([1, 2, 3])

# mapa con los sensores


def main():
    n = 10
