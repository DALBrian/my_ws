import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

master_1 = modbus_tcp.TcpMaster(host="192.168.255.1")
master_1.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[0, 0, 0, 0])

a = input("s = stop: ")
if a == 's':
    master_1.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 1, 1])
    master_1._do_close