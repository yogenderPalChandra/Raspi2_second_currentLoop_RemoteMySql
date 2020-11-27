import time
import board
import busio
import pandas as pd

#import time
import sys
import sqlite3
#from time import sleep

#import adafruit_ads1x15.ads1015 as ADS
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import MySQLdb as db


import paho.mqtt.client as paho
import time
import json


HOST = "10.208.8.122"
PORT = 3306
USER = "yogi"
PASSWORD = "bittoo"
DB = "TemaccessToRemoteRp2"
'''
try:
    connection = db.Connection(host=HOST, port=PORT,
                               user=USER, passwd=PASSWORD, db=DB)

    c = connection.cursor()
    c.execute("SELECT * from temSensor")
    result = c.fetchall()
    for item in result:
        print (item)

except Exception as e:
    print (e)
'''
connectionL = db.connect(host="10.208.8.121",
                     user="yogi",
                     passwd="bittoo",
                     db="allSensors")

mqttClient=paho.Client()
mqttClient.tls_set('/etc/ssl/certs/DST_Root_CA_X3.pem')
mqttClient.username_pw_set(username='gen1_yogi',password='uceeb123456mqtt')
mqttClient.connect('data.hydronics40.com',8883,keepalive=1)

#c = conn.cursor()
connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)

cR = connectionR.cursor()
cL =connectionL.cursor()


#print (cR.column_names)
#date=time.strftime("%Y-%m-%d ")
#t=time.strftime("%H:%M:%S")

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

ads.gain = 1


cL.execute('DROP TABLE IF EXISTS flowReadings;')
print ('table deleted')


cL.execute('CREATE TABLE flowReadings(id INT AUTO_INCREMENT PRIMARY KEY, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, flowHP FLOAT, flowLoad FLOAT);')


#df = pd.DataFrame(columns=[i for i in range (0, 22)])
#df = pd.DataFrame()
#print (df)


lol=[[], [], []]
flowRateLoad  = []
sensorsName =  [ 'Ambient', 'topTesting', 'bottomtesting', 'topSoure', 'loadTank', 'topTestingLoadCircuit', 'loadMix', 'bottomSource', 'bottomTestingloadCircuit', \
'temStrat1', 'temStrat3', 'temStratt5', 'temStratt7', 'temStratt9', 'temStratt11', 'temStratt13', 'temStratt15', 'temStratt17', 'temStratt19', 'flowHp', 'flowLoad']
dictAllSensors = dict([(key, []) for key in sensorsName])
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage))
    #connection.commit()
    chan1 = AnalogIn(ads, ADS.P0)
    chan2 = AnalogIn(ads, ADS.P1)

    chan1Vol = chan1.voltage
    chan1curr = chan1Vol/159.42

    chan2Vol = chan2.voltage
    chan2curr=chan2Vol/159.65
    #flow1 = ((chan1Vol/159.42)*1000 -4)/16*1000
    flow1 = ((chan1Vol/159.42)-0.003956)/0.0000159
    flow2 = ((chan2Vol/159.65)*1000 -4)/16*4000
    cL.execute("INSERT INTO flowReadings(flowHp, flowLoad) VALUES(%s, %s)", (flow2, flow1))
    connectionL.commit()
    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))
    print('flow rates load is = ',chan1Vol, chan1curr,flow1 )
    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    print (result[0])
    x = [len(resu) for resu in result]
    #print (x)
    #dictAllSensorsLastValue = dict([(key, '') for key in sensorsName])
    #dictAllSensorsLastValue= dict.fromkeys(sensorsName)
    dictAllSensorsLastValue = {}
    for b, n in enumerate (range (2,21)):
        #dictAllSensorsLastValue = dict([(key, None) for key in sensorsName])
        #dictAllSensorsLastValue = {}
        dictAllSensorsLastValue[sensorsName[b]]=result[0][n]
    dictAllSensorsLastValue['flowLoad']=flow1
    dictAllSensorsLastValue['flowHp']=flow2
    mqttClient.publish('cz/cvut/uceeb/rp5/gen1/gen1_yogi/Yogi',json.dumps(dictAllSensorsLastValue),qos=0)
    #print (dictAllSensorsLastValue)
    #dictAllSensorsLastValue = dict([(key, '') for key in sensorsName])
    '''
    for i, j in zip (sensorsName, range (2,21)):
        dictAllSensors[i].append(result[0][j])
    dictAllSensors['flowLoad'].append(flow1)
    dictAllSensors['flowHp'].append(flow2)
    '''
    #print (dictAllSensors)
    #print (result)
    #lol[0].append(result)
    id = result[0][0]
    #print (lol[0])
    #print (id, lol[0][-1][0][0])
    #lol[0].append(result)
    #lol[1].append(chan1.value)
    #lol[2].append(chan2.value)
    '''
    flowRateLoad.append(flow1)
    #print ('flow rate is',flowRateLoad)
    if lol[0] ==[] or id < lol[0][-1][0][0] :
        lol[0].append(result)
        #print (lol)
        lol[1].append(flow1)
        lol[2].append(flow2)
    elif lol[0] != [] and id > lol[0][-1][0][0]:
        #print ('dsdafdafdsatrue')
        #print (id,lol[0][-1][0][0])
        lol[0].append(result)
        lol[1].append(flow1)
        lol[2].append(flow2)
    #print (list[0][-1][0][0])
    print (lol)
    '''
    #mqttClient.publish('cz/cvut/uceeb/rp5/gen1/gen1_yogi/Yogi',json.dumps(dictAllSensors),qos=0)
    print('________________________________________________________________')
    time.sleep(0.5)
'''
lol=[[], [], []]
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    #lol[0].append(result)
    id = result[0][0]
    #print (id, lol[0][-1][0][0])
    #lol[0].append(result)
    #lol[1].append(chan1.value)
    #lol[2].append(chan2.value)
    if lol[0] ==[]:
        lol[0].append(result)
        print (lol)
    elif  id > lol[0][-2][0][0]:
        print ('dsdafdafdsatrue')
        print (id,lol[0][-2][0][0])
        lol[0].append(result)
        lol[1].append(chan1.value)
        lol[2].append(chan2.value)

    #print (list[0][-1][0][0])
    #print (lol)
    print('________________________________________________________________')
    time.sleep(0.5)
'''
'''
lol=[[], [], []]
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    #lol[0].append(result)
    id = result[0][0]
    #print (id, lol[0][-1][0][0])
    #lol[0].append(result)
    #lol[1].append(chan1.value)
    #lol[2].append(chan2.value)
    if lol[0] ==[]:
           lol[0].append(result)
           print (lol)
           if  id > lol[0][-2][0][0]:
               print ('dsdafdafdsatrue')
               print (id,lol[0][-2][0][0])
               lol[0].append(result)
               lol[1].append(chan1.value)
               lol[2].append(chan2.value)

    #print (list[0][-1][0][0])
    #print (lol)
    print('________________________________________________________________')
    time.sleep(0.5)
'''
'''
lol=[[], [], []]
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    lol[0].append(result)
    id = result[0][0]
    #print (id, lol[0][-1][0][0])
    #lol[0].append(result)
    #lol[1].append(chan1.value)
    #lol[2].append(chan2.value)
    if lol[0] ==[]:
           lol[0].append(result)
           print (lol)
           if  id > lol[0][-2][0][0]:
              print ('dsdafdafdsatrue')
              print (id,lol[0][-2][0][0])
              lol[0].append(result)
              lol[1].append(chan1.value)
              lol[2].append(chan2.value)

    #print (list[0][-1][0][0])
    #print (lol)
    print('________________________________________________________________')
    time.sleep(0.5)

'''


'''
list=[[], [], []]
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    list[0].append(result)
    id = result[0][0]
    #print (id, list[0][-1][0][0])
    #list[0].append(result)
    #list[1].append(chan1.value)
    #list[2].append(chan2.value)
    if id ==0:
        print ('true')
        list[0].append(result)
        print (list[0][-1][0][0])
    elif id > 0 and id != list[0][-2][0][0]:
       # print ('true')
        #print (id,list[0][-1][0][0])
        list[0].append(result)
        list[1].append(chan1.value)
        list[2].append(chan2.value)

    #print (list[0][-1][0][0])
    print (list)
    print('________________________________________________________________')
    time.sleep(0.5)
'''

'''
list=[[], [], []]
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    list[0].append(result)
    id = result[0][0]
    print (id, list[0][-1][0][0])
    #list[0].append(result)
    #list[1].append(chan1.value)
    #list[2].append(chan2.value)
    if id ==0:
        list[0].append(result)

    if id != list[0][-2][0][0]:
        print ('true')
        print (id,list[0][-1][0][0])
        list[0].append(result)
        list[1].append(chan1.value)
        list[2].append(chan2.value)

    #print (list[0][-1][0][0])
    print (list)
    print('________________________________________________________________')
    time.sleep(0.5)
'''

'''
list=[[], [], []]
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    id = result[0][0]
    print(id)
    if id not in list[0][0]:
    list[0].append(result)
    list[1].append(chan1.value)
    list[2].append(chan2.value)
    #print (list[0][0])
    #df = pd.DataFrame()
    #df.append(result)
    #df = pd.DataFrame(result, columns=[i for i in range (0, 21)])
    #print (df)
    #df = pd.read_sql("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1", con=connectionR)
    #print (df)
    #cL.execute("INSERT INTO  sensorsAll(Temp1d4, Temp2d5, Temp3d6, \
    #Temp4d13,  Temp5d19, Temp6d26, Temp7d21,Temp8d20, Temp9d16, \
    #Temp10d12,Temp11d1,Temp12d7, Temp13d8,Temp14d24,\
    #Temp15d23, Temp16d18,Temp17d15, Temp18d14,Temp19d2, flowHp, flowLoad  SELECT * FROM temSensor );")
    #df = pd.DataFrame(columns=[i for i in range (0, 22)])
    #for item in result:
        #df = pd.read_sql(, con=db_connection)
        #df = pd.DataFrame(columns=[i for i in range (0, 22)])
        #df.append(item)
        #print (df)
        #print (item)
    print('________________________________________________________________')
    time.sleep(1)
'''

'''
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    #df = pd.read_sql("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1", con=connectionR)
    #print (df)
    #cL.execute("INSERT INTO  sensorsAll(Temp1d4, Temp2d5, Temp3d6, \
    #Temp4d13,  Temp5d19, Temp6d26, Temp7d21,Temp8d20, Temp9d16, \
    #Temp10d12,Temp11d1,Temp12d7, Temp13d8,Temp14d24,\
    #Temp15d23, Temp16d18,Temp17d15, Temp18d14,Temp19d2, flowHp, flowLoad  SELECT * FROM temSensor );")
    df = pd.DataFrame(columns=[i for i in range (0, 22)])
    for item in result:
        #df = pd.read_sql(, con=db_connection)
        #df = pd.DataFrame(columns=[i for i in range (0, 22)])
        df.append(item)
        print (df)
        print (item)
    print('________________________________________________________________')

'''
'''
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    #x = [i for i in result]
    #print (x)
    #print (type(result))
    #df = pd.read_sql("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1", con=connectionR)
    #print (df)
    #cL.execute("INSERT INTO  sensorsAll(Temp1d4, Temp2d5, Temp3d6, \
    #Temp4d13,  Temp5d19, Temp6d26, Temp7d21,Temp8d20, Temp9d16, \
    #Temp10d12,Temp11d1,Temp12d7, Temp13d8,Temp14d24,\
    #Temp15d23, Temp16d18,Temp17d15, Temp18d14,Temp19d2, flowHp, flowLoad  SELECT * FROM temSensor );")
    for item in result:
        #df = pd.read_sql(, con=db_connection)
        #df = pd.DataFrame(columns=[i for i in range (0, 22)])
        #df.append(item)
        #print (df)
        #print (item)
    print('________________________________________________________________')

    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)
'''
'''
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    df = pd.read_sql("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1", con=connectionR)
    #cL.execute("INSERT INTO  sensorsAll(Temp1d4, Temp2d5, Temp3d6, \
    #Temp4d13,  Temp5d19, Temp6d26, Temp7d21,Temp8d20, Temp9d16, \
    #Temp10d12,Temp11d1,Temp12d7, Temp13d8,Temp14d24,\
    #Temp15d23, Temp16d18,Temp17d15, Temp18d14,Temp19d2, flowHp, flowLoad  SELECT * FROM temSensor );")
    #for item in result:
        #df = pd.read_sql(, con=db_connection)
        #df = pd.DataFrame(columns=[i for i in range (0, 22)])
        #df.append(item)
        #print (df)
        #print (item)
    print('________________________________________________________________')

    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)
'''

'''
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    #cL.execute("INSERT INTO  sensorsAll(Temp1d4, Temp2d5, Temp3d6, \
    #Temp4d13,  Temp5d19, Temp6d26, Temp7d21,Temp8d20, Temp9d16, \
    #Temp10d12,Temp11d1,Temp12d7, Temp13d8,Temp14d24,\
    #Temp15d23, Temp16d18,Temp17d15, Temp18d14,Temp19d2, flowHp, flowLoad  SELECT * FROM temSensor );")
    for item in result:

        #df = pd.DataFrame(columns=[i for i in range (0, 22)])
        #df.append(item)
        print (df)
        print (item)
    print('________________________________________________________________')

    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)
'''
'''
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    #cL.execute("INSERT INTO  sensorsAll(Temp1d4, Temp2d5, Temp3d6, \
    #Temp4d13,  Temp5d19, Temp6d26, Temp7d21,Temp8d20, Temp9d16, \
    #Temp10d12,Temp11d1,Temp12d7, Temp13d8,Temp14d24,\
    #Temp15d23, Temp16d18,Temp17d15, Temp18d14,Temp19d2, flowHp, flowLoad  SELECT * FROM temSensor );")
    for item in result:
        print (len(item))
    print('________________________________________________________________')

    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)

'''

'''
cL.execute('CREATE TABLE sensorsAll(id INT AUTO_INCREMENT PRIMARY KEY, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Temp1d4 FLOAT, Temp2d5 FLOAT, Temp3d6 FLOAT, \
Temp4d13 FLOAT,  Temp5d19 FLOAT, Temp6d26 FLOAT, Temp7d21 FLOAT,Temp8d20 FLOAT,Temp9d16 FLOAT, \
Temp10d12 FLOAT,Temp11d1 FLOAT,Temp12d7 FLOAT, Temp13d8 FLOAT,Temp14d24 FLOAT,\
Temp15d23 FLOAT, Temp16d18 FLOAT,Temp17d15 FLOAT, Temp18d14 FLOAT,Temp19d2 FLOAT);')


while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    #connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connectionR = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    cR = connectionR.cursor()
    #c.execute("SELECT * from temSensor")
    cR.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = cR.fetchall()
    for item in result:
        print (item)
    print('________________________________________________________________')

    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)
'''

'''
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))


    connection = db.Connection(host=HOST, port=PORT,user=USER, passwd=PASSWORD, db=DB)
    c = connection.cursor()
    #c.execute("SELECT * from temSensor")
    c.execute("SELECT * FROM temSensor ORDER BY id DESC LIMIT 1")
    result = c.fetchall()

    for item in result:
        print (item)


    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)
'''

'''
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))

    print('________________________________________________________________')

    for item in result:
        print (item)


    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)

'''

'''
while True:
    #c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    connection.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))
    print('________________________________________________________________')


    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)


'''
