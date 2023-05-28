import sys
import serial

#add logging capability
import logging

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu

from threading import Timer
import time



#正反轉.速度控制
def go100():
    logger.info(master.execute(1, 6, 610, output_value=-45))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(2, 6, 610, output_value=600))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(3, 6, 610, output_value=40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(4, 6, 610, output_value=-600))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
def back100():
    logger.info(master.execute(1, 6, 610, output_value=45))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(2, 6, 610, output_value=-600))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(3, 6, 610, output_value=-40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(4, 6, 610, output_value=600))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
def right100():
    logger.info(master.execute(1, 6, 610, output_value=50))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(2, 6, 610, output_value=-40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(3, 6, 610, output_value=40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(4, 6, 610, output_value=-50))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
def left100():
    logger.info(master.execute(1, 6, 610, output_value=-50))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(2, 6, 610, output_value=40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(3, 6, 610, output_value=-40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(4, 6, 610, output_value=50))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
def cw100():
    logger.info(master.execute(1, 6, 610, output_value=-45))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(2, 6, 610, output_value=-40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(3, 6, 610, output_value=40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(4, 6, 610, output_value=50))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
def ccw100():
    logger.info(master.execute(1, 6, 610, output_value=45))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(2, 6, 610, output_value=40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(3, 6, 610, output_value=-40))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(4, 6, 610, output_value=-50))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
def test1():
    logger.info(master.execute(1, 6, 610, output_value=45))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(3, 6, 610, output_value=45))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
def stop():
    logger.info(master.execute(1, 6, 610, output_value=0))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(2, 6, 610, output_value=0))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(3, 6, 610, output_value=0))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))
    logger.info(master.execute(4, 6, 610, output_value=-0))#(設備通訊位置,寫入=6,參數代碼(十進位),輸出值(十進位))

def current_value():
    a = logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 702, 1))
    print(a[0])
    
logger = modbus_tk.utils.create_logger("console")
PORT = 'COM7'#USB連接阜位址
master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
master.set_timeout(1.0)
master.set_verbose(True)
logger.info("connected")   
print("請輸入任意字母")
abc=input()
while (abc!=''):
    try:
        if abc=='w':
            go100()
            abc=input()

        elif abc=='s':
            back100()
            abc=input()

        elif abc=='a':
            left100()
            abc=input()

        elif abc=='d':
            right100()
            abc=input()

        elif abc=='e':
            cw100()
            abc=input()

        elif abc=='q':
            ccw100()
            abc=input()

        elif abc=='c':
            stop()
            abc=input()
        elif abc=='q':
            test1()
            abc=input()
        else:
            stop()
            print("stopping")
            break
    except:
        print("something wrong")
        abc=input()
print("結束程式")