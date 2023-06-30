import pandas as ps
import numpy as np
from scipy.spatial.transform import Rotation as R
filename = "M1_timesort.csv"
filepath = "/home/dal/my_ws/src/KF_standarlized/Timesort0629/"
lidar_std = 0.1
gyro_std = 0.1
acc_std = 0.1

class readcsv():
    def __init__(self):
        print("Reading CSV data!")
        self.kf = kalmanfilter()
        self.car_start = False
    def __del__(self):
        print("Deleting")
    def readcsv(self):
        usecols = ['time', 'cmd_vel', 'imuacc_x', 'imuacc_y','imuacc_z', 'imuori_x',
                    'imuori_y', 'imuori_z', 'imuori_w' 'odompos_x', 'odompos_y',  
                    'odomori_z', 'odomori_w']
        print("Read data from file: ", filepath + filename)
        self.csvdata = ps.read_csv(filepath+filename)
        self.csvdata = self.csvdata.dropna(axis=0, how='any')
        print(self.csvdata.head())
        self.datalength = self.csvdata.shape[0]
        self.datawidth = self.csvdata.shape[1]
        print("Input data shape: ", self.csvdata.shape)
    def playcsv(self):
        print("Playcsv")
        for i in range(0, self.datalength): # Detect the vehicle start
            if(self.csvdata["cmd_vel"][i] != 0):
                # print("cmd_vel: ", self.csvdata["cmd_vel"][i], "at index: ", i)
                self.car_start = True
            if (self.csvdata["imuacc_x"][i] != 0 and not self.car_start): # Detect IMU data or Odometry data
                # print("imuacc_x: ", self.csvdata["imuacc_x"][i], "at index: ", i)
                self.kf.predict(self.csvdata["imuacc_x"][i], self.csvdata["imuacc_y"][i], self.csvdata["imuacc_z"][i], 
                                self.csvdata["imuori_x"][i], self.csvdata["imuori_y"][i], self.csvdata["imuori_z"][i], self.csvdata["imuori_w"][i]) #Prediction should has a higher update rate
                

            elif (self.csvdata["odompos_x"][i] != 0 and self.car_start):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                # print("odompos_x: ", self.csvdata["odompos_x"][i], "at index: ", i)
                # imu_quat_x = self.csvdata["imuori_x"][i]
                # imu_quat_y = self.csvdata["imuori_y"][i]
                # imu_quat_z = self.csvdata["imuori_z"][i]
                # imu_quat_w = self.csvdata["imuori_w"][i]
                # imu_pose = R.from_quat([imu_quat_x, imu_quat_y, imu_quat_z, imu_quat_w])
                # print("imu_pose: ", imu_pose.as_euler('xyz', degrees=True))
                odom_quat_x = self.csvdata["odomori_x"][i]
                odom_quat_y = self.csvdata["odomori_y"][i]
                odom_quat_z = self.csvdata["odomori_z"][i]
                odom_quat_w = self.csvdata["odomori_w"][i]
                odom_pose = R.from_quat([odom_quat_x, odom_quat_y, odom_quat_z, odom_quat_w])
                print("odom_quat_w: ", odom_pose.as_euler('xyz', degrees=True))
                self.kf.update(self.csvdata["odompos_x"][i], self.csvdata["odompos_y"][i], self.csvdata["odompos_z"][i], 
                               self.csvdata["odomori_x"][i], self.csvdata["odomori_y"][i], self.csvdata["odomori_z"][i], self.csvdata["odomori_w"][i], )#Update should has a higher update rate      
    def rot(self):
        print("rot")

class kalmanfilter():
    def __init__(self):
        print("Initialize Kalman filter!")
        #State and Covariance
        self.X = np.array({}) #state matrix
        self.P_bel = np.array([0.1])
        #Prediction step
        
        
        self.Q = np.array([0.1]) #Prediction input noise
        ##Update step
        self.H = np.array([[1.0], 
                           [1.0], 
                           [1.0]])#Relationship between state and measurement
        self.R = np.array([[0.01, 0., 0.],
                        [0., 0.02, 0.],
                        [0., 0., 0.04]]) #Update noise(Measurement) noise
        self.I = np.array([1.0]) #unit matrix
    def __del__(self):
        print("Deleting KF!")
    def predict(self, accx, accy, accz, orix, oriy, oriz, oriw):
        print("Received imu msg accx: ", accx, "accy: ", accy, "accz: ", accz, "\n orix: ", orix, "oriy ", oriy, "oriz: ", oriz, "oriw: ", oriw)
        self.X = #Physic model
        self.F = np.array([]) #what?
        self.P = self.F * self.P * np.transpose(self.F) + self.Q
    def update(self, posx, posy, posz, orix, oriy, oriz, oriw):
        print("Received odom msg posx: ", posx, "posy: ", posy, "posz: ", posz, "\n orix: ", orix, "oriy ", oriy, "oriz: ", oriz, "oriw: ", oriw)
        z = np.array([]) #Measurement input
        z_hat = self.H * self.X
        y = z - z_hat
        S = self.H * self.P * np.transpose(self.H) + self.R
        K = self.P * np.transpose(self.H) * np.linalg.inv(S)
        
        self.X = self.X + K * y
        self.P = (np.eye() - K * self.H) * self.P

if __name__ == '__main__':
    read = readcsv()
    read.readcsv()
    read.playcsv()
    