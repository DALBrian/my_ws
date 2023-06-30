import pandas as ps
import numpy as np
filename = "M1.csv"
filepath = "/home/dal/KF_standarlized/data/"
lidar_std = 0.1
gyro_std = 0.1
acc_std = 0.1

class KF():
    def __init__(self):
        print("init")

    def __del__(self):
        print("del")
    def readcsv(self):
        usecols = ['time', 'cmd_vel', 'imuacc_x', 'imuacc_y','imuacc_z', 'imuori_x',
                    'imuori_y', 'imuori_z', 'imuori_w' 'odompos_x', 'odompos_y',  
                    'odomori_z', 'odomori_w']
        self.csvdata = ps.read_csv(filepath+filename)
        self.data = self.data.dropna(axis=0, how='any')
        print(self.csvdata.head())
        datasize = self.csvdata.size / len(usecols)
    def predict(self):
        print("predict")
    def update(self):
        print("update")