import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
filename = "M1_timesort.csv"
filepath = "/home/dal/data/KF_standarlized/Timesort0629/"
lidar_std = 0.1
gyro_std = 0.1
acc_std = 0.1
'''
@author: Small Brian
@date: 2023/07/03
@brief: First version of Extended Kalman Filter for master thesis. Work with KF_standarlized data.
@detail: Copycat-version of sensor-fusion-lidar-imu repo.
'''
class readcsv():
    def __init__(self):
        print("Reading CSV data!")
        self.kf = kalmanfilter()
        self.car_start = False
        self.isStart = False
        self.initialdata = np.array([])
    def __del__(self):
        print("Deleting")
    def readcsv(self):
        print("Read data from file: ", filepath + filename)
        self.csvdata = ps.read_csv(filepath+filename)
        self.csvdata = self.csvdata.dropna(axis=0, how='any')
        # print(self.csvdata.head())
        self.datalength = self.csvdata.shape[0]
        self.datawidth = self.csvdata.shape[1]
        print("Input data shape: ", self.csvdata.shape)
        self.get_cov()
        self.get_mean()
        self.get_var()
    def playcsv(self):
        print("Playing CSV")
        index = 0
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
                # print("odom_quat_w: ", odom_pose.as_euler('xyz', degrees=True))
                self.kf.update(self.csvdata["odompos_x"][i], self.csvdata["odompos_y"][i], self.csvdata["odompos_z"][i], 
                               self.csvdata["odomori_x"][i], self.csvdata["odomori_y"][i], self.csvdata["odomori_z"][i], self.csvdata["odomori_w"][i], )#Update should has a higher update rate      
        self.kf.save_to_csv()
    def get_mean(self):
        self.initialmean = np.array([np.mean(self.csvdata["imuacc_x"][:300]), np.mean(self.csvdata["imuacc_y"][:300]), 
                          np.mean(self.csvdata["imuacc_z"][:300]), np.mean(self.csvdata["imuori_x"][:300]), 
                          np.mean(self.csvdata["imuori_y"][:300]), np.mean(self.csvdata["imuori_z"][:300]), 
                          np.mean(self.csvdata["imuori_w"][:300]), np.mean(self.csvdata["odompos_x"][:30]), 
                          np.mean(self.csvdata["odompos_y"][:30]), np.mean(self.csvdata["odompos_z"][:30]), 
                          np.mean(self.csvdata["odomori_x"][:30]), np.mean(self.csvdata["odomori_y"][:30]), 
                          np.mean(self.csvdata["odomori_z"][:30]), np.mean(self.csvdata["odomori_w"][:30]), 
                          ])
        return self.initialmean 
    def get_cov(self):
        self.initialcov = np.array([np.cov(self.csvdata["imuacc_x"][:300]), np.cov(self.csvdata["imuacc_y"][:300]), 
                          np.cov(self.csvdata["imuacc_z"][:300]), np.cov(self.csvdata["imuori_x"][:300]), 
                          np.cov(self.csvdata["imuori_y"][:300]), np.cov(self.csvdata["imuori_z"][:300]), 
                          np.cov(self.csvdata["imuori_w"][:300]), np.cov(self.csvdata["odompos_x"][:30]), 
                          np.cov(self.csvdata["odompos_y"][:30]), np.cov(self.csvdata["odompos_z"][:30]), 
                          np.cov(self.csvdata["odomori_x"][:30]), np.cov(self.csvdata["odomori_y"][:30]), 
                          np.cov(self.csvdata["odomori_z"][:30]), np.cov(self.csvdata["odomori_w"][:30]), 
                          ])
        return self.initialcov
    def get_var(self):
        self.initialvar = np.array([np.var(self.csvdata["imuacc_x"][:300]), np.var(self.csvdata["imuacc_y"][:300]), 
                          np.var(self.csvdata["imuacc_z"][:300]), np.var(self.csvdata["imuori_x"][:300]), 
                          np.var(self.csvdata["imuori_y"][:300]), np.var(self.csvdata["imuori_z"][:300]), 
                          np.var(self.csvdata["imuori_w"][:300]), np.var(self.csvdata["odompos_x"][:30]), 
                          np.var(self.csvdata["odompos_y"][:30]), np.var(self.csvdata["odompos_z"][:30]), 
                          np.var(self.csvdata["odomori_x"][:30]), np.var(self.csvdata["odomori_y"][:30]), 
                          np.var(self.csvdata["odomori_z"][:30]), np.var(self.csvdata["odomori_w"][:30]), 
                          ])
        return self.initialvar
class kalmanfilter():
    def __init__(self):
        self.is_initial = False
        print("Initialize Kalman filter!")
        #State and Covariance
        self.X = np.array([]) #Initial state matrix
        self.P = np.array([]) #Initial covariance matrix
        self.P_bel = np.array([0.1])
        #Prediction step
        self.Q = np.array([0.1]) #Prediction input noise
        ##Update step
        self.H = np.array([[1.]])#Relationship between state and measurement
        self.R = np.array([[0.04]]) #Update noise(Measurement) noise
        self.I = np.array([1.0]) #unit matrix
        self.history = np.array([[0, 0],])
    def __del__(self):
        print("Deleting KF!")
    def predict(self, accx, accy, accz, orix, oriy, oriz, oriw):
        # print("Received imu msg accx: ", accx, "accy: ", accy, "accz: ", accz, "\n orix: ", orix, "oriy ", oriy, "oriz: ", oriz, "oriw: ", oriw)
        yaw = oriz
        print("Predction: ", yaw)
        if (self.is_initial == False):
            # Use first measurement to initialize
            self.X = np.array([[yaw]]) #State
            self.P = np.array([[0]])#Covariance 
            self.is_initial = True
        else:
            self.X = self.X + yaw #Physic model, TODO
            self.F = np.array([[1]]) #Process model matrix
            self.P = np.matmul(self.F, np.matmul(self.P, np.transpose(self.F))) + self.Q
            result = np.array([[self.X[0][0], self.P[0][0]], ])
            print("Result: ", result.shape)
            print("history: ", self.history.shape)
            self.history = np.concatenate((self.history, result))
    def update(self, posx, posy, posz, orix, oriy, oriz, oriw):
        yaw = oriz
        print("Update: ", yaw)
        if (self.is_initial == False):
            # Use first measurement to initialize
            self.X = np.array([[yaw]]) #State
            self.P = np.array([[0]])#Covariance 
            self.is_initial = True
        else:
            print("Received odom msg posx: ", posx, "posy: ", posy, "posz: ", posz, "\n orix: ", orix, "oriy ", oriy, "oriz: ", oriz, "oriw: ", oriw)
            z = np.array([[yaw]]) #Measurement input
            z_hat = self.H * self.X #Current state to update measurement
            y = z - z_hat
            S = self.H * self.P * np.transpose(self.H) + self.R
            K = self.P * np.transpose(self.H) * np.linalg.inv(S)
            print("1")
            self.X = self.X + K * y
            print("2")
            self.P = (np.eye(1) - K * self.H) * self.P
            print("3")
            result = np.array([[self.X[0][0], self.P[0][0]], ])
            print("Result: ", result.shape)
            print("history: ", self.history.shape)
            self.history = np.concatenate((self.history, result))
    def save_to_csv(self):
        print("Start saving data to csv.")
        df = pd.DataFrame(self.history)
        df.columns = ['Result_X', 'Result_Cov']
        df.to_csv("/home/dal/my_ws/src/KF_standarlized/result/" + "KF_TEST0703" + '.csv')
        print("Done! Save file to: ", "/home/dal/my_ws/src/KF_standarlized/result/" + "KF_TEST0703" + ".csv")
if __name__ == '__main__':
    read = readcsv()
    temp = read.readcsv()
    read.playcsv()
    print("Program End!")