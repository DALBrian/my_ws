#!/usr/bin/env python3
###Modified to cater Ubuntu. 20230315###
import sys
sys.path.append('../include')

import driver_connection
import driver_read
import driver_setting
import chassic_kinematic_v2

# test driver_connection and driver_read
driver = driver_connection.driver_connection()
read = driver_read.driver_read(driver)
move = chassic_kinematic_v2.driver_kinekatic(driver)

while(True):
    direction = input("Enter direction: ")
    if direction == "w":
        print("Moving forward")
        move.fwd()
    elif direction == "x":
        print("Moving backward")
        move.bwd()
    elif direction == "a":
        print("Moving left")
        move.left()
    elif direction == "d":
        print("Moving right")
        move.right()
    elif direction == "r":
        print("Rotating CCW ")
        move.rot_ccw()
    elif direction == "t":
        print("Rotating CW ")
        move.rot_cw()
    elif direction == "s":
        print("Stopping")
        move.stop()
    elif direction == "q":
        print("left forward")
        move.left_fwd()
    elif direction == "e":
        print("right forward")
        move.right_fwd()
    elif direction == "z":
        print("left back")
        move.left_bwd()
    elif direction == "c":
        print("right back")
        move.right_bwd()
    elif direction =="exit":
        break
    else:
        print("Stopping")
        move.stop()
driver.driver_close()