import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
PORT = '/dev/ttyUSB0'
master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
master.set_timeout(1.0)
master.set_verbose(1.0)
# master.execute(1, 6, 610, output_value=40)
DO_status = dict()
for i in range(1, 5):
    print("Allocating DI status of motor no.", i)
    index = str(i)
    sta = master.execute(i, cst.READ_HOLDING_REGISTERS, 706, 1)[0]
    if sta is not None:
        DO_status['motor' + index + ' output status'] = sta
print(DO_status)

master._do_close()