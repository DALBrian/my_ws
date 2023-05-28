import numpy as np
param = {}	
param["car_size_x"] = 1.7
param["car_size_y"] = 2.1
XY = param["car_size_x"] * param["car_size_y"]
R = 0.34
H = np.zeros([4,3])
velocity = np.zeros([3, 1])
rotating_speed = np.array([])
H[0][0] = 1 #re-check the motor number and matrix sequence.
H[0][1] = 1
H[0][2] = -XY
H[1][0] = 1
H[1][1] = 1
H[1][2] = XY
H[2][0] = 1
H[2][1] = -1
H[2][2] = -1* XY
H[3][0] = 1
H[3][1] = -1
H[3][2] =  XY
print("H matrix: ", H)
velocity[0][0] = 0.5
velocity[1][0] = 0
velocity[2][0] = 0
print("velocity matrix: ", velocity)
rotating_speed = np.matmul(H, velocity) / R
print("rotating_speed matrix: ", rotating_speed)