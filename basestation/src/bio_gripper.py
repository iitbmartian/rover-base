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


# SIGINT handler
def sigint_handler_arm(signal, frame):
    Arm_RPi.arm_stop()
    sys.exit(0)


class Arm_RPi:

    def __init__(self, pin1,pin2):
        self.pin1=pin1
        self.pin2=pin2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1, GPIO.OUT)
        
        # self.gripper = GPIO.PWM(pin1, 50)
        # self.gripper_rot = GPIO.PWM(pin2, 50)
        # self.gripper.start(11.5)
        # self.gripper_rot.start(0)
        # self.last_position = 5.5
        sleep(1)
        self.gripper_desc = {'name': "Gripper", 'speed': 0,
                             'direction': "stop", 'duty': 2}  # Claw1M1; Stop: 0, Up: 1, Down: -1
        
    # def update_arm_steer(self):
    #     self.rungripper(self.gripper_desc)
        

    def arm_callback(self, inp):
        self.gripper_desc['speed'], self.gripper_desc['direction'] = int(inp.gripper.speed), inp.gripper.direction


        # self.rungripper(self.gripper_desc)
        # self.rungripper_rot(self.gripper_rot_desc)

    def arm_stop(self):
        rospy.loginfo('Arm_RPi: ' + "Arm_RPi commanded to stop")
        
        GPIO.output(self.pin1,GPIO.LOW)
        GPIO.output(self.pin2,GPIO.LOW)


    def rungripper(self, cmd_dict):
        # if cmd_dict['direction'] == "stop":
        #     self.gripper.ChangeDutyCycle(0)
        if self.gripper_desc['direction'] == 'forward':
            GPIO.output(self.pin1,GPIO.HIGH)
            GPIO.output(self.pin2,GPIO.LOW)
            
        elif self.gripper_desc['direction'] == 'backward':
            GPIO.output(self.pin1,GPIO.LOW)
            GPIO.output(self.pin2,GPIO.HIGH)
        elif self.gripper_desc['direction'] == 'stop':
            GPIO.output(self.pin1,GPIO.LOW)
            GPIO.output(self.pin2,GPIO.LOW)






def enable_motors():
    print()
    enb_all = input("Enable Motors? ")
    if enb_all == "y" or enb_all == "Y" or enb_all == "yes" or enb_all == "Yes":
        enable_gripper = True
        
    else:
        enable_gripper = False
        
    return enable_gripper


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler_arm)

    rospy.init_node("Arm_RPi_Node")
    rospy.loginfo("Starting Arm_RPi_Node")
    iter_time = rospy.Rate(1)
    enable_gripper = enable_motors()

    if enable_gripper:
        rospy.loginfo("Connected to RPi for Bio_Gripper")

    # initialising Arm Object-------------------
    Arm_RPi = Arm_RPi(positive_pin,negative_pin)
    Arm_RPi.arm_stop()

    rospy.loginfo("Subscribing to /rover/arm_directives...")
    rospy.Subscriber("/rover/arm_directives", arm_msg, Arm_RPi.arm_callback)
    rospy.loginfo("Subscribed to /rover/arm_directives")
    run_time = rospy.Rate(10)
    while not rospy.is_shutdown():
        Arm_RPi.rungripper()
        run_time.sleep()
