#!/usr/bin/env python3import sys
import time
import tty, termios
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp


if __name__ == "__main__":
    master_1 = modbus_tcp.TcpMaster(host="192.168.1.149")
    if master_1 is not None:
        print("TCP connection successful")
    master_1.set_timeout(5.0)
    index = 30000
    # try:
    while index < 50000:
        print("This is the ", index, "time")
        spd = master_1.execute(1, 4 , index, 1)[0]
        if spd != 0:    
            print("This is the ", index, "time, reading: ",spd)
        index += 1
    # except :
    #     print("This is the ", index, "time")
    #     index += 1
#   except:
#         master_1._do_close()
#         index += 1
#         print("This is the ", index, "time")