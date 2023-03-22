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
logger.info("connected")   
#%%
command_speed = master.execute(4, cst.READ_HOLDING_REGISTERS, 700, 1)
command_torque =  master.execute(4, cst.READ_HOLDING_REGISTERS, 702, 1)
#%%
last_error_1 =  master.execute(1, cst.READ_HOLDING_REGISTERS, 707, 1)
last_error_2 =  master.execute(2, cst.READ_HOLDING_REGISTERS, 707, 1)
last_error_3 =  master.execute(3, cst.READ_HOLDING_REGISTERS, 707, 1)
last_error_4 =  master.execute(4, cst.READ_HOLDING_REGISTERS, 707, 1)
#%%
error_1 = list()
error = master.execute(1, cst.READ_HOLDING_REGISTERS, 708, 1)
error_1.append(error[0])
error = master.execute(1, cst.READ_HOLDING_REGISTERS, 709, 1)
error_1.append(error[0])
error = master.execute(1, cst.READ_HOLDING_REGISTERS, 710, 1)
error_1.append(error[0])
error = master.execute(1, cst.READ_HOLDING_REGISTERS, 711, 1)
error_1.append(error[0])
#%%
error_2 = list()
error = master.execute(2, cst.READ_HOLDING_REGISTERS, 708, 1)
error_2.append(error[0])
error = master.execute(2, cst.READ_HOLDING_REGISTERS, 709, 1)
error_2.append(error[0])
error = master.execute(2, cst.READ_HOLDING_REGISTERS, 710, 1)
error_2.append(error[0])
error = master.execute(2, cst.READ_HOLDING_REGISTERS, 711, 1)
error_2.append(error[0])
#%%
error_3 = list()
error = master.execute(3, cst.READ_HOLDING_REGISTERS, 708, 1)
error_3.append(error[0])
error = master.execute(3, cst.READ_HOLDING_REGISTERS, 709, 1)
error_3.append(error[0])
error = master.execute(3, cst.READ_HOLDING_REGISTERS, 710, 1)
error_3.append(error[0])
error = master.execute(4, cst.READ_HOLDING_REGISTERS, 711, 1)
error_3.append(error[0])
#%%
error_4 = list()
error = master.execute(4, cst.READ_HOLDING_REGISTERS, 708, 1)
error_4.append(error[0])
error = master.execute(4, cst.READ_HOLDING_REGISTERS, 709, 1)
error_4.append(error[0])
error = master.execute(4, cst.READ_HOLDING_REGISTERS, 710, 1)
error_4.append(error[0])
error = master.execute(4, cst.READ_HOLDING_REGISTERS, 711, 1)
error_4.append(error[0])
#%%
for i in range(1, 5):
    print( master.execute(i, cst.READ_HOLDING_REGISTERS, 712, 1))

#%%
print(master.execute(1, cst.READ_HOLDING_REGISTERS, 709, 1))
print(master.execute(1, cst.READ_HOLDING_REGISTERS, 710, 1))
print(master.execute(1, cst.READ_HOLDING_REGISTERS, 711, 1))
print("the command speed: ", command_speed)
print("the command torque: ", command_torque[0] * 0.01)
# print("last_error: ", last_error)
#%% given command
for i in [1,2,3,4]:
    master.execute(i, 6, 26, output_value=1)
#%%
master._do_close()