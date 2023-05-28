"""
Created on Mon Apr 11 17:16:43 2023

@author: Small Brian
@email: dalbobo3122@gmail.com
"""
class driver_kinekatic():
    """
    This class is used to control the movement of the vehicle, 
    and the speed commands are the same for each motor.
    Motor speed vary from 0~3000(RPM), divided the reduction ratio(10) will be the true speed.
    Direction of rotation is positive when vehicle moving forward(when facing the vehicle, KUKA controller on the right)
    If one of the motor speed needs to be modified, change the code as the following example:
        ex: self.master.execute(modbus_location, 6, command(Pn610=610), output_value = speed)
            self.master.execute(1, 6, 610, output_value = motor_speed1)
            self.master.execute(2, 6, 610, output_value = motor_speed2)
            self.master.execute(3, 6, 610, output_value = motor_speed3)
            self.master.execute(4, 6, 610, output_value = motor_speed4)
    """
    def __init__(self, driver_connection):
        self.master = driver_connection.master
        # print("Current motor speed: ", output_value = self.basespeed)

    def fwd(self, speed = 45):
        for i in range(1, 5):
            self.master.execute(i, 6, 610, output_value = speed)
            
    def bwd(self, speed = 45):
        for i in range(1, 5):
            self.master.execute(i, 6, 610, output_value = speed * -1)
            
    def left(self, speed = 45):
        for i in [1, 2]:
            self.master.execute(i, 6, 610, output_value = speed)
        for i in [3, 4]:
            self.master.execute(i, 6, 610, output_value = speed * -1)
       
    def right(self, speed = 45):
        for i in [1, 2]:
            self.master.execute(i, 6, 610, output_value = speed * -1)
        for i in [3, 4]:
            self.master.execute(i, 6, 610, output_value = speed)
        
    def rot_cw(self, speed = 45):
        for i in [1, 3]:
            self.master.execute(i, 6, 610, output_value = speed * -1)
        for i in [2, 4]:
            self.master.execute(i, 6, 610, output_value = speed)
        
    def rot_ccw(self, speed = 45):
        for i in [1, 3]:
            self.master.execute(i, 6, 610, output_value = speed)
        for i in [2, 4]:
            self.master.execute(i, 6, 610, output_value = speed * -1)
    def left_fwd(self, speed = 45):
        for i in [1, 2]:
            self.master.execute(i, 6, 610, output_value = 0)
        for i in [3, 4]:
            self.master.execute(i, 6, 610, output_value = speed)
    def right_fwd(self, speed = 45):
        for i in [1, 2]:
            self.master.execute(i, 6, 610, output_value = speed)
        for i in [3, 4]:
            self.master.execute(i, 6, 610, output_value = 0)
    def left_bwd(self, speed = 45):
        for i in [1, 2]:
            self.master.execute(i, 6, 610, output_value = speed * -1)
        for i in [3, 4]:
            self.master.execute(i, 6, 610, output_value = 0)
    def right_bwd(self, speed = 45):
        for i in [1, 2]:
            self.master.execute(i, 6, 610, output_value = 0)
        for i in [3, 4]:
            self.master.execute(i, 6, 610, output_value = speed * -1)
    def stop(self):
        for i in range(1, 5):
            self.master.execute(i, 6, 610, output_value = 0)
        