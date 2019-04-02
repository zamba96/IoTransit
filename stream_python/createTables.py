import psycopg2

import sys

# PostgreSQL connection
connection = None
cursor = None
try:
    connection = psycopg2.connect(user="postgres",
                                  password="12345",
                                  host="54.149.247.97",
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
    st = "DROP TABLE lecturas"
if numSensores == -2:
    st = "DELETE FROM lecturas"
else:
    st = '''CREATE TABLE lecturas(TS INT PRIMARY KEY NOT NULL'''
    for i in range(numSensores):
        st += ",\nS{} INT".format(i)
    st += ");"
print(st)
cursor.execute(st)
connection.commit()


cursor.close()
connection.close()
