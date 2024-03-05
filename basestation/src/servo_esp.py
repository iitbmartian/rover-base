#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
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
   
    sys.exit(0)


class Servo_Esp:
    def __init__(self):
       self.servo_number=0
       self.gpio_high=31
       self.gpio_low=1
       self.angle=0
    def update_servo(self):
        
        self.serial_send(self.servo_number,self.angle,self.gpio_high,self.gpio_low)

    # def servo_callback(self, inp):
    #     self.angle=inp.data
        
    # def arm_stop(self):
    #     rospy.loginfo('Arm_RPi: ' + "Arm_RPi commanded to stop")
    #     # ser.close()
    #     # self.gripper_rot.ChangeDutyCycle(7)
    #     # self.gripper.ChangeDutyCycle(0)

    def serial_send(self,servo_number,angle,gpio_high,gpio_low):
        servo_number_cmd=f"{servo_number:02}"
        angle_cmd=f"{angle:003}"
        gpio_high_cmd=f"{gpio_high:02}"
        gpio_low_cmd=f"{gpio_low:02}"
    
    
        command=servo_number_cmd+angle_cmd+gpio_high_cmd+gpio_low_cmd
        command=command+'\n'
        ser.write(command.encode())
        print("Sent "+command)
        print("done")
        
        print(ser.read(6).decode())
        
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
    Servo_Esp = Servo_Esp()
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = PORT
    ser.open()
    # Arm_Esp.arm_stop()

    rospy.loginfo("Subscribing to /rover/arm_directives...")
    # rospy.Subscriber("/rover/arm_directives", Float32, Servo_Esp.servo_callback)
    rospy.loginfo("Subscribed to /rover/arm_directives")
    run_time = rospy.Rate(10)
    while not rospy.is_shutdown():
        Servo_Esp.update_servo()
        run_time.sleep()


