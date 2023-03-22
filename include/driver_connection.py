# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:58:58 2023

@author: Small Brian
@email: dalbobo3122@gmail.com
"""
###Modified to cater Ubuntu. 20230315###
import serial
import modbus_tk
import modbus_tk.modbus_rtu as modbus_rtu
class driver_connection():
    def __init__(self, PORT = '/dev/ttyUSB1'):
        self.active = False
        self.master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        self.master.set_timeout(1.0)
        self.master.set_verbose(True)
        self.active = True
        print("Driver connection establish successfully!")
    def __del__(self):
        driver_connection.driver_close(self)
    def driver_close(self):
        if (self.master._do_close()):
            self.active = False
            print("Driver connection closed")
