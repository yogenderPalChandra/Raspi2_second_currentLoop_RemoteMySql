import time
import board
import busio

#import time
import sys
import sqlite3
#from time import sleep

#import adafruit_ads1x15.ads1015 as ADS
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn



#import paramiko
#from paramiko import SSHClient

conn = sqlite3.connect('FlowSensors.db')
c = conn.cursor()
date=time.strftime("%Y-%m-%d ")
t=time.strftime("%H:%M:%S")

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

ads.gain = 1

# Create single-ended input on channel 0
#chan = AnalogIn(ads, ADS.P0, ADS.P1)
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)
#print (chan.value)
#print (chan.voltage)
#Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)
#print (chan.value, chan.voltage)
#print("{:>5}\t{:>5}".format('raw', 'v'))


c.execute('DROP TABLE IF EXISTS  flowReadings;')
print ('table deleted')

c.execute('CREATE TABLE flowReadings(id INTEGER PRIMARY KEY AUTOINCREMENT, flowHp NUMERIC, \
flowLoad NUMERIC, Date DATE,Time TIME);')
conn.commit()
while True:
    c.execute("INSERT INTO flowReadings(flowHp, flowLoad, Date,Time) VALUES(?,?,?,?)", (chan2.voltage, chan1.voltage, date,t))
    conn.commit()

    print('flow HP:',"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage), '\n\n')
    print('flow load:',"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage, '\n\n'))
    print('________________________________________________________________')


    #print("{:>5.3f}".format(chan.voltage))
    time.sleep(0.5)

