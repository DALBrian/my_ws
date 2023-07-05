import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
filename = "mapbuilding_1"
filepath = "/home/dal/data/KF_standarlized/0629/"
newfilename = "mapbuilding_1_processed"

if __name__ == '__main__':
    print("Read data from file: ", filepath + filename + '.csv')
    csvdata = pd.read_csv(filepath+filename+'.csv')
    csvdata = csvdata.dropna(axis=0, how='any')
    length, width = csvdata.shape
    result = np.zeros([length, width])
    record = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0], ])
    Yaw = 0
    for i in range(0, length):
        #magnetic meter
        imu_ori_x = csvdata['imuori_x'][i]
        imu_ori_y = csvdata['imuori_y'][i]
        imu_ori_z = csvdata['imuori_z'][i]
        imu_ori_w = csvdata['imuori_w'][i]
        if (imu_ori_x != 0 or imu_ori_y != 0 or imu_ori_z != 0 or imu_ori_w != 0):
            mag = R.from_quat([csvdata['imuori_x'][i], csvdata['imuori_y'][i],
                            csvdata['imuori_z'][i], csvdata['imuori_w'][i]])
            mag_pose = mag.as_euler('xyz')
        else:
            mag_pose = np.array([0, 0, 0])
        #acceleratormeter
        acc_x = csvdata['imuacc_x'][i]
        acc_y = csvdata['imuacc_y'][i]
        acc_z = csvdata['imuacc_z'][i]
        #gyro
        ang_x = csvdata['imuang_x'][i]
        ang_y = csvdata['imuang_y'][i]
        ang_z = csvdata['imuang_z'][i]
        #lidar
        odom_ori_x = csvdata['odomori_x'][i]
        odom_ori_y = csvdata['odomori_y'][i]
        odom_ori_z = csvdata['odomori_z'][i]
        odom_ori_w = csvdata['odomori_w'][i]
        if (odom_ori_x != 0 or odom_ori_y != 0 or odom_ori_z != 0 or odom_ori_w != 0):
            lidar = R.from_quat([odom_ori_x, odom_ori_y, 
                                odom_ori_z, odom_ori_w])
            lidar_pose = lidar.as_euler('xyz')
        else:
            lidar_pose = np.array([0, 0, 0])

        if (i < length-1):
            Yaw += ((csvdata['time'][i+1]- csvdata['time'][i]) * 0.5 *
                    (csvdata['imuang_z'][i] + csvdata['imuang_z'][i+1]))
            
        msg = np.array([[csvdata['time'][i], mag_pose[0], mag_pose[1], mag_pose[2], lidar_pose[0], 
                         lidar_pose[1], lidar_pose[2], 
                         acc_x, acc_y, acc_z, ang_x, ang_y, ang_z, Yaw], ])
        print("record: ", record.shape)
        print("msg: ", msg.shape)
        record = np.concatenate((record, msg))
        
    df = pd.DataFrame(record)
    df.columns = ['time', 'mag_pose0', 'mag_pose1', 'mag_pos2', 'lid_pos0', 'lid_pos1', 'lid_pos2', 
                  'acc_x', 'acc_y', 'acc_z', 'ang_x', 
                    'ang_y', 'ang_z', 'Yaw']
    df.to_csv(filepath+ filename + '_processed' + '.csv')
    print("Done! Save file to: ", filepath + filename + '_processed' + ".csv")