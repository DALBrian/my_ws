import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
filename = "M1_processed.csv"
filepath = "/home/dal/data/KF_standarlized/0629/"
lidar_std = 0.1
gyro_std = 0.1
acc_std = 0.1
'''
@author: Small Brian
@date: 2023/07/03
@brief: Use quatternion to euler instead
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
        print("Read data from file: ", filepath + filename + '.csv')
        self.csvdata = pd.read_csv(filepath+filename)
        self.csvdata = self.csvdata.dropna(axis=0, how='any')
        # print(self.csvdata.head())
        self.datalength = self.csvdata.shape[0]
        self.datawidth = self.csvdata.shape[1]
        print("Input data shape: ", self.csvdata.shape)
        return self.csvdata
    def playcsv(self):
        print("Playing CSV")
        index = 0
        for i in range(0, self.datalength): # Detect the vehicle start
            if(self.csvdata["cmd_vel"][i] != 0):
                # print("cmd_vel: ", self.csvdata["cmd_vel"][i], "at index: ", i)
                self.car_start = True
            if (self.csvdata["imuacc_x"][i] != 0 and not self.car_start): # Detect IMU data or Odometry data
                # print("imuacc_x: ", self.csvdata["imuacc_x"][i], "at index: ", i)
                r = R.from_quat([self.csvdata["imuori_x"][i], self.csvdata["imuori_y"][i],
                                          self.csvdata["imuori_z"][i], self.csvdata["imuori_w"][i]])
                imu_pose = r.as_euler()
                self.kf.predict(imu_pose) #Prediction should has a higher update rate
            elif (self.csvdata["odompos_x"][i] != 0 and self.car_start):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                
                r = R.from_quat([self.csvdata["odomori_x"][i], self.csvdata["odomori_y"][i],
                                          self.csvdata["odomori_z"][i], self.csvdata["odomori_w"][i]])
                odom_pose = r.as_euler()
                self.kf.update(odom_pose)#Update should has a higher update rate      
        self.kf.save_to_csv()
    def playcsv2(self):
        for i in range(0, self.datalength-3):
            if (self.csvdata["ang_z"][i] != 0):
                self.kf.predict(self.csvdata["Yaw"][i])
            elif (self.csvdata["lid_pos2"][i] != 0):
                self.kf.update(self.csvdata["lid_pos2"][i], self.csvdata["ang_z"][i-2], 
                               self.csvdata["mag_pos2"][i-2])

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
        self.H = np.array([[1.], 
                           [1.], 
                           [1.]])#Relationship between state and measurement
        self.R = np.array([[0.01, 0., 0.],
                            [0., 0.02, 0.],
                            [0., 0., 0.04]]) #Update noise(Measurement) noise
        self.I = np.array([1.0]) #unit matrix
        self.history = np.array([[0, 0],])
    def __del__(self):
        print("Deleting KF!")
    def predict(self, Yaw):
        # print("Received imu msg accx: ", accx, "accy: ", accy, "accz: ", accz, "\n orix: ", orix, "oriy ", oriy, "oriz: ", oriz, "oriw: ", oriw)
        print("Predction: ", gyro)
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
    def update(self, lidar, gyro, mag):
        if (self.is_initial == False):
            # Use first measurement to initialize
            self.X = np.array([[yaw]]) #State
            self.P = np.array([[0]])#Covariance 
            self.is_initial = True
        else:
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
    data = read.readcsv()
    kf = kalmanfilter()
    X = np.array([[0.0], ]) #Initial state matrix
    P = np.array([[0.0],]) #Initial covariance matrix
    P_bel = np.array([[0.1], ])
    #Prediction step
    Q = np.array([[0.1], ]) #Prediction input noise
    ##Update step
    H = np.array([[1.], 
                [1.], 
                [1.]])#Relationship between state and measurement
    R = np.array([[0.01, 0., 0.],
                        [0., 0.02, 0.],
                        [0., 0., 0.04]]) #Update noise(Measurement) noise
    I = np.array([[1.0], ]) #unit matrix
    
    history = np.array([[0, 0, 0],])
    for i in range(0, data.shape[0] - 3):
        if (data["ang_z"][i] != 0):
            # kf.predict(data["Yaw"][i])
            X[0] = X[0] + data["ang_z"][i] #Physic model, TODO
            F = np.array([[1.0]]) #Process model matrix
            P = np.matmul(F, np.matmul(P, np.transpose(F))) + Q
            result = np.array([[X[0][0], P[0][0], 0],])
            print("Result: ", result.shape)
            print("history: ", history.shape)
            history = np.concatenate((history, result))

        elif (data["lid_pos2"][i] != 0):
            lidar = data["lid_pos2"][i]
            Yaw = data["Yaw"][i+2]
            mag = data["mag_pos2"][i+2]
            # kf.update(data["lid_pos2"][i], data["ang_z"][i-2], data["mag_pos2"][i-2])    
            z = np.array([[lidar],
                          [Yaw],
                          [mag]]) #Measurement input
            z_hat = np.matmul(H, X) #Current state to update measurement
            y = z - z_hat
            S = np.matmul(H, np.matmul(P, np.transpose(H))) + R
            K = np.matmul(P, np.matmul(np.transpose(H), np.linalg.inv(S)))
            X = X + np.matmul(K, y)
            P = np.matmul((np.eye(1) - np.matmul(K, H)), P)
            result = np.array([[X[0][0], P[0][0], 1], ])
            print("Result: ", result.shape)
            print("history: ", history.shape)
            history = np.concatenate((history, result))
    print("Start saving data to csv.")
    df = pd.DataFrame(history)
    df.columns = ['Result_X', 'Result_Cov', 'index']
    df.to_csv("/home/dal/my_ws/src/KF_standarlized/result/" + filename + ".csv")
    print("Done! Save file to: ", "/home/dal/my_ws/src/KF_standarlized/result/" + filename + ".csv")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.grid(True)
    ax1.plot(range(history.shape[0]), history[:,0])
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.grid(True)
    ax2.legend(["Proposed"])
    ax2.plot(range(data['Yaw'].shape[0]), data['Yaw'])
    plt.show()
    print("Program End!")