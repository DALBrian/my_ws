import numpy as np
import matplotlib.pyplot as plt
import pandas as ps
"""
    @author: Small Brian
    @bridf: Fitting a cos(x) and cos(x+180) function
"""

if __name__ =="__main__":   
    dt = 0.1
    time = np.arange(0, 3, dt)
    x1 = np.array([])
    x2 = np.array([])
    result = np.array([])
    x1 = np.cos(time)
    x2 = np.cos(time + np.pi)
    result = np.append(time, x1)
    result = np.append(result, x2)
    result = np.reshape(result,(3, 30))
    # np.savetxt("/home/dal/my_ws/src/path.csv", result, delimiter=",")

    DF = ps.DataFrame(result)
    DF.to_csv("/home/dal/my_ws/src/path.csv", index=False)
        