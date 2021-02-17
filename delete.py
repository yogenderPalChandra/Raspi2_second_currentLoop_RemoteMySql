from struct import *

import time
import struct
from pyModbusTCP.client import ModbusClient

import math
def number_to_bytes(number):
     nibble_count = int(math.log(number, 256)) + 1
     hex_string = '{:0{}x}'.format(number, nibble_count * 2)
     return bytearray.fromhex(hex_string)

def countTotalBits(num):
     # convert number into it's binary and
     # remove first two characters 0b.
     binary = bin(num)[2:]
     print(len(binary))
while True:
    # TCP auto connect on first modbus request
    c = ModbusClient(host="10.208.8.125", port=502, auto_open=True)

    regs = c.read_input_registers(19026, 2)
    a = regs[0]
    #a = number_to_bytes(regs[0])
    countTotalBits(a)
    #b = number_to_bytes(regs[1])
    b = regs[1]
    countTotalBits(b)
    print (a,b)
    #fL = struct.unpack('!f', bytes.fromhex('{0:02x}'.format(a) + '{0:02x}'.format(b)))
    mypack = pack('>HH',a,b)
    #print (mypack)
    fl = unpack('>f', mypack)
    #print (a,b)
    #print (fL)
    print (fl)
    time.sleep(0.1)

