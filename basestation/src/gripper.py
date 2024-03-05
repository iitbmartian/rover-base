#!/usr/bin/env python3

import rospy
from rover_msgs.msg import arm_msg
from serial.serialutil import SerialException as SerialException
import signal
import sys
import os
from time import sleep
import serial
import serial.tools.list_ports as ports

PORT='/dev/myUSB'

# SIGINT handler
def sigint_handler_arm(signal, frame):
    Arm_Esp.arm_stop()
    sys.exit(0)


class Arm_Esp:
    def __init__(self):
       # self.gripper.start(0)
       # self.gripper_rot.start(0)
        self.gripper_cmd=0
        self.gripper_rot_cmd=0
        self.gripper_desc = {'name': "Gripper", 'speed': 0,
                                  'direction': "stop", 'aduty': 12, 'cduty': 2}  # Claw1M1; Stop: 0, Up: 1, Down: -1
        self.gripper_rot_desc = {'name': "Gripper Rotation", 'speed': 0,
                               'direction': "stop"}  # Claw1M2; Stop: 0, Extend: 1, Contract: -1
    def update_arm_steer(self):
        self.rungripper(self.gripper_desc)
        self.rungripper_rot(self.gripper_rot_desc)
        # self.gripper_cmd=int(input("Enter gripper_cmd:"))
        # self.gripper_rot_cmd=int(input("Enter gripper_rot_cmd:"))
        self.serial_send(self.gripper_cmd,self.gripper_rot_cmd)

    def arm_callback(self, inp):
        self.gripper_desc['speed'], self.gripper_desc['direction'] = int(inp.gripper.speed), inp.gripper.direction
        self.gripper_rot_desc['speed'], self.gripper_rot_desc['direction'] = int(inp.gripper_rot.speed), inp.gripper_rot.direction
    def arm_stop(self):
        rospy.loginfo('Arm_RPi: ' + "Arm_RPi commanded to stop")
        # ser.close()
        # self.gripper_rot.ChangeDutyCycle(7)
        # self.gripper.ChangeDutyCycle(0)
    def rungripper(self, cmd_dict):
        if cmd_dict['direction'] == "stop":
            # self.gripper.ChangeDutyCycle(0)
            self.gripper_cmd=0
        if cmd_dict['direction'] == "forward":
            # self.gripper_clock()
            self.gripper_cmd=1
            rospy.loginfo('Arm: ' + cmd_dict['name'] + ' commanded to move in Direction = 1')
        if cmd_dict['direction'] == "backward":
            # self.gripper_anticlock()
            self.gripper_cmd=2
            rospy.loginfo('Arm: ' + cmd_dict['name'] + ' commanded to move in Direction = -1')

    def rungripper_rot(self, cmd_dict):
        if cmd_dict['direction'] == "stop":
            # self.gripper_rot.ChangeDutyCycle(7)
            self.gripper_rot_cmd=0

        if cmd_dict['direction'] == "forward":
            # self.gripper_rot.ChangeDutyCycle(2)
            self.gripper_rot_cmd=1
            rospy.loginfo('Arm: ' + cmd_dict['name'] + ' commanded to move in Direction = 1')
        if cmd_dict['direction'] == "backward":
            # self.gripper_rot.ChangeDutyCycle(10)
            self.gripper_rot_cmd=2
            rospy.loginfo('Arm: ' + cmd_dict['name'] + ' commanded to move in Direction = -1')
    def serial_send(self,a,b):
       
        sum=0
        
        if sum==0:
            command="a"
        elif sum==1:
            command="b"
        elif sum==2:
            command="c"
        elif sum==10:
            command="d"
        elif sum==11:
            command="e"
        elif sum==12:
            command="f"
        elif sum==20:
            command="g"
        elif sum==21:
            command="h"
        elif sum==22:
            command="i"
        command=command+'\n'
        ser.write(command.encode())
        print("Sent "+command)
        
        # print(ser.read(6).decode())
        
        # try:
        #     ser.readline()
        #     print("Received "+ser.read().decode())
        # except:
        #     print("Nothing received")
def enable_motors():
    print()
    enb_all = input("Enable Motors? ")
    if enb_all == "y" or enb_all == "Y" or enb_all == "yes" or enb_all == "Yes":
        enable_gripper = True
        enable_gripper_rotation = True
    else:
        enable_gripper = False
        enable_gripper_rotation = False
    return enable_gripper, enable_gripper_rotation

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler_arm)
    # com_ports = list(ports.comports())  # create a list of com ['COM1','COM2']
    # for i in com_ports:
	#     print(i.device)  # returns 'COMx'
    rospy.init_node("Arm_Esp_Node")
    rospy.loginfo("Starting Arm_Esp_Node")
    iter_time = rospy.Rate(1)
    enable_gripper, enable_gripper_rotation = enable_motors()

    if enable_gripper_rotation and enable_gripper:
        rospy.loginfo("Connected to Esp for Gripper and Gripper Rotation")

    # initialising Arm Object-------------------
    Arm_Esp = Arm_Esp()
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = PORT
    ser.open()
    Arm_Esp.arm_stop()

    rospy.loginfo("Subscribing to /rover/arm_directives...")
    rospy.Subscriber("/rover/arm_directives", arm_msg, Arm_Esp.arm_callback)
    rospy.loginfo("Subscribed to /rover/arm_directives")
    run_time = rospy.Rate(10)
    while not rospy.is_shutdown():
        Arm_Esp.update_arm_steer()
        run_time.sleep()




