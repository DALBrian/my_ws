import sys
import serial

#add logging capability
import logging

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu

from threading import Timer
import time

PORT = "/dev/ttyUSB1"#USB連接阜位址
master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
master.set_timeout(1.0)
master.set_verbose(True)
function_number = 211
value = 40
print("Function no: ", function_number, " set as: ", value)
for i in range(1, 5):
    print("Modbus address: ", i)
    info = master.execute(i, 6, function_number, output_value=value)
    print(info)
master._do_close()
print("結束程式")