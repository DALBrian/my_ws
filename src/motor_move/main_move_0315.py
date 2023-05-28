#!/usr/bin/env python3
###Modified to cater Ubuntu. 20230315###
import sys
# sys.path.append('../include')

import driver_connection
import driver_read
import driver_setting
import chassic_kinematic

# test driver_connection and driver_read
driver = driver_connection.driver_connection()
read = driver_read.driver_read(driver)
move = chassic_kinematic.chassic_kinematic(driver)

while(True):
    direction = input("Enter direction: ")
    if direction == "w":
        print("Moving forward")
        move.fwd()
    elif direction == "s":
        print("Moving backward")
        move.bwd()
    elif direction == "a":
        print("Moving left")
        move.left()
    elif direction == "d":
        print("Moving right")
        move.right()
    elif direction == "q":
        print("Rotating CCW ")
        move.rot_ccw()
    elif direction == "e":
        print("Rotating CW ")
        move.rot_cw()
    elif direction == "x":
        print("Stopping")
        move.stop()
    elif direction =="exit":
        break
    else:
        print("Stopping")
        move.stop()
driver.driver_close()