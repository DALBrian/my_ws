import sys
import serial

#add logging capability
import logging

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu

logger = modbus_tk.utils.create_logger("console")
PORT = 'COM7'#USB連接阜位址
master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
master.set_timeout(1.0)
master.set_verbose(True)
print("connected")   
#%% motor1
master.execute(1, 6, 610, output_value = 40)
#%% motor1 stop
master.execute(1, 6, 610, output_value = 0)
#%% motor1 reverse
master.execute(1, 6, 5, output_value = 1)


#%% motor2
master.execute(2, 6, 610, output_value = 50)
#%% motor2 stop
master.execute(2, 6, 610, output_value = 0)
#%% motor2 reverse
master.execute(2, 6, 5, output_value = 0)


#%% motor3
master.execute(3, 6, 610, output_value = 50)
#%% motor3 stop
master.execute(3, 6, 610, output_value = 0)
#%% motor3 reverse
master.execute(3, 6, 5, output_value = 1)


#%% motor4
master.execute(4, 6, 610, output_value = 50)
#%% motor4 stop
master.execute(4, 6, 610, output_value = 0)
#%% motor4 reverse
master.execute(4, 6, 5, output_value = 0)
#%%
for i in range(1, 5):
    master.execute(i, 6, 610, output_value = -40)
#%%
for i in range(1, 5):
    master.execute(i, 6, 610, output_value = 0)


#%%
master._do_close()