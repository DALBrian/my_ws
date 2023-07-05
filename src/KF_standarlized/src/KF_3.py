#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
filepath = "/home/dal/data/KF_standarlized/0629/"
filename = "M1_withAng"
saveto = "/home/dal/my_ws/src/KF_standarlized/result/"
init_pos_std = 0.1
init_vel_std = 0.1
accel_std = 0.1
pos_std = 0.1
yaw_std = 0.1
vel_std = 0.1
def read_csv():
    csvdata = pd.read_csv(filepath+filename+'.csv')
    csvdata = csvdata.dropna(axis=0, how='any')
    return csvdata
def save_csv(history):
    print("Start saving data to csv.")
    df = pd.DataFrame(history)
    df.columns = ['Result_X', 'Result_Cov']
    df.to_csv(saveto + filename +"_KF3" + '.csv')
    print("Done! Save file to: ", saveto + filename + "_KF3" + ".csv")
#%%
if __name__ == '__main__':
    data = read_csv()
    history = np.zeros([1, 4])
    print("Data keys: ", data.keys)
    #state
    X = np.zeros([4,1]) #(Px, Py, Yaw, V)
    P = np.diag(np.array([init_pos_std*init_pos_std,
                        init_pos_std*init_pos_std,
                        init_vel_std*init_vel_std,
                        init_vel_std*init_vel_std]))
    length = 1000
    Px_last = 0
    Py_last = 0
    for i in range(1, length):
        if (data['imuori_w'][i] != 0):
            #Prediction
            dt = data['time'][i] - data['time'][i-1]
            F = np.zeros(3,3) #State transition matrix, TODO, Jacobian?
            Q = np.diag(np.array([(0.5*dt*dt),(0.5*dt*dt),dt,dt]) * (accel_std*accel_std))
            # X = np.matmul(F, X) #or direct calculate?
            X[0] = X[0] + X[3] * dt * np.cos(X[2]) + 0.5 * data['imuacc_x'] * dt * dt
            X[1] = X[1] + X[3] * dt * np.sin(X[2]) + 0.5 * data['imuacc_y'] * dt * dt
            X[2] = X[2] + data['imuang_z'] * dt
            X[3] = X[3] + dt * np.sqrt((data['imuacc_x'][i] * data['imuacc_x'][i]) + (data['imuacc_y'][i] * data['imuacc_y'][i]))
            P = np.matmul(F, np.matmul(P, np.linalg.inv(F))) + Q
            # msg = np.append(X)
            history = np.stack([history, np.transpose(X)])
        
        elif (data['odomori_w'][i] != 0):
            # Update
            dt = data['time'][i] - data['time'][i-1]
            Px = data['odompos_x'][i]
            Py = data['odompos_y'][i]
            odom = R.from_quat([data['odomori_x'][i], data['odomori_y'][i], data['odomori_z'][i], data['odomori_w'][i]])
            Roll, Pitch, Yaw = odom.as_euler('xyz')
            vel = np.sqrt(pow((Px - Px_last),2) + pow((Py - Py_last), 2))
            z = np.array([[Px], [Py], [Yaw], [vel]]) # Measurement
            H = np.eye(4) #TODO, Jacobian?
            z_hat = np.matmul(H, X)
            y = z_hat - z
            R = np.diag([pow(pos_std,2), pow(pos_std,2), pow(yaw_std,2), pow(vel_std,2)])
            S = np.matmul(H, np.matmul(P, np.linalg.inv(H)) + R)
            K = np.matmul(P, np.matmul(np.transpose(H), np.linalg.inv(S)))
            X = X + np.matmul(K, y)
            P = np.matmul((np.eye(4) - np.matmul(K, H)), P)
            Px_last = Px
            Py_last = Py
            # msg = np.append(X)
            history = np.stack([history, np.transpose(X)])
    save_csv(history)