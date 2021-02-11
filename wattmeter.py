import time
import struct
from pyModbusTCP.client import ModbusClient

import math
def number_to_bytes(number):
     nibble_count = int(math.log(number, 256)) + 1
     hex_string = '{:0{}x}'.format(number, nibble_count * 2)
     return bytearray.fromhex(hex_string)

while True:
    # TCP auto connect on first modbus request
    c = ModbusClient(host="10.208.8.125", port=502, auto_open=True)

    regs = c.read_input_registers(19026, 2)
    a = regs[0]
    #a = number_to_bytes(regs[0])

    #b = number_to_bytes(regs[1])
    b = regs[0]
    fl = struct.unpack('!f', bytes.fromhex('{0:02x}'.format(a) + '{0:02x}'.format(b)))
    print (a,b)

    print (fl)
    time.sleep(0.1)

'''
import struct
from pyModbusTCP.client import ModbusClient
# TCP auto connect on first modbus request
c = ModbusClient(host="10.208.8.125", port=502, auto_open=True)

regs = c.read_input_registers(4884, 2)

a = regs[0]
b= regs[1]

fl = struct.unpack('!f', bytes.fromhex('{0:02x}'.format(a) + '{0:02x}'.format(b)))

print (fl)



if regs:
    print(regs)
    #result = regs.registers
    #print (result)
else:
    print("read error")
'''
