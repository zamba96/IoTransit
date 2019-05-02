import psycopg2

import sys
import json


def kafkaServer():
    with open('config/ip.json') as json_file:
        data = json.load(json_file)
        print(data['psql'])
        return data['psql']


kafkaServer = kafkaServer()

# PostgreSQL connection
connection = None
cursor = None
try:
    connection = psycopg2.connect(user="postgres",
                                  password="12345",
                                  host=kafkaServer,
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

print(sys.argv[1])
numSensores = int(sys.argv[1])

if numSensores == -1:
    print("[INFO] -1: borrando tablas")
    st = "DROP TABLE lecturas"
    st2 = "DROP TABLE pred"
elif numSensores == -2:
    print("[INFO] -2: limpiando tablas")
    st = "DELETE FROM lecturas"
    st2 = "DELETE FROM pred"
else:
    print("[INFO] creando tablas")
    st = '''CREATE TABLE lecturas(TS INT PRIMARY KEY NOT NULL'''
    for i in range(numSensores):
        st += ",\nS{} INT".format(i)
    st += ");"
    st2 = '''CREATE TABLE pred(TS INT PRIMARY KEY NOT NULL'''
    for i in range(numSensores):
        st2 += ",\nS{} FLOAT".format(i)
    st2 += ");"
print(st)
cursor.execute(st)
cursor.execute(st2)
connection.commit()


cursor.close()
connection.close()
