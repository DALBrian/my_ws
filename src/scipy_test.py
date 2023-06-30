from scipy.spatial.transform import Rotation as R
import numpy as np

if __name__ == '__main__':
    r = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])
    print("As matrix: ", r.as_matrix())
    print("As euler: ", r.as_euler('zyx', degrees=True))
    r.as_euler('xyz', degrees=True)
    print("As quat: ", r.as_quat())
    #########
    # print(R.from_rotvec([0, 0, 0]).as_quat())
    # r = R.from_rotvec(np.pi/6 * np.array([0, 0, 1]))
    # print("As matrix: ", r.as_matrix())
    # print("As euler: ", r.as_euler('xyz', degrees=True))
    # print("As quat: ", r.as_quat())
