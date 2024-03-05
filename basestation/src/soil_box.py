#!/usr/bin/env python3

import rospy
from rover_msgs.msg import arm_msg
from serial.serialutil import SerialException as SerialException
import signal
import sys
import os
import RPi.GPIO as GPIO
from time import sleep
positive_pin=22
negative_pin=27
time_open=3
time_close=3


# SIGINT handler
def sigint_handler_arm(signal, frame):
    Arm_RPi.arm_stop()
    sys.exit(0)


class Arm_RPi:

    def __init__(self, pin1,pin2,time_open,time_close):
        self.pin1=pin1
        self.pin2=pin2
        self.time_open=time_open
        self.time_close=time_close
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        
        # self.soil_box = GPIO.PWM(pin1, 50)
        # self.soil_box_rot = GPIO.PWM(pin2, 50)
        # self.soil_box.start(11.5)
        # self.soil_box_rot.start(0)
        # self.last_position = 5.5
        sleep(1)
        self.soil_box_desc = {'name': "soil_box",
                             'direction': "stop"}  # Claw1M1; Stop: 0, Up: 1, Down: -1
        
    # def update_arm_steer(self):
    #     self.runsoil_box(self.soil_box_desc)
        

    def arm_callback(self, inp):
        self.soil_box_desc['direction'] = inp.soil_box.direction
        if self.soil_box_desc['direction'] == 'forward':
            GPIO.output(self.pin1,GPIO.HIGH)
            GPIO.output(self.pin2,GPIO.LOW)
            rospy.sleep(self.time_open)
            
        elif self.soil_box_desc['direction'] == 'backward':
            GPIO.output(self.pin1,GPIO.LOW)
            GPIO.output(self.pin2,GPIO.HIGH)
            rospy.sleep(self.time_close)
            


        # self.runsoil_box(self.soil_box_desc)
        # self.runsoil_box_rot(self.soil_box_rot_desc)

    def arm_stop(self):
        rospy.loginfo('Arm_RPi: ' + "Soil_Box commanded to stop")
        
        GPIO.output(self.pin1,GPIO.LOW)
        GPIO.output(self.pin2,GPIO.LOW)







def enable_motors():
    print()
    enb_all = input("Enable Motors? ")
    if enb_all == "y" or enb_all == "Y" or enb_all == "yes" or enb_all == "Yes":
        enable_soil_box = True
        
    else:
        enable_soil_box = False
        
    return enable_soil_box


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler_arm)

    rospy.init_node("Soil_Box_Node")
    rospy.loginfo("Starting Soil_Box_Node")
    iter_time = rospy.Rate(1)
    enable_soil_box = enable_motors()

    if enable_soil_box:
        rospy.loginfo("Connected to RPi for Bio_soil_box")

    # initialising Arm Object-------------------
    Arm_RPi = Arm_RPi(positive_pin,negative_pin,time_open,time_close)
    Arm_RPi.arm_stop()

    rospy.loginfo("Subscribing to /rover/arm_directives...")
    rospy.Subscriber("/rover/arm_directives", arm_msg, Arm_RPi.arm_callback)
    rospy.loginfo("Subscribed to /rover/arm_directives")
    rospy.spin()

