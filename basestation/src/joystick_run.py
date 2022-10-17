#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Joy

arm_pub = rospy.Publisher('/rover/arm_directives', Float64MultiArray, queue_size=1)
drive_pub = rospy.Publisher('/rover/drive_directives', Float64MultiArray, queue_size=1)


def joy_callback(joy_inp):
    joy_inp_axes = joy_inp.axes
    joy_inp_buttons = joy_inp.buttons

    arm_out = [80 if x % 2 == 1 else 0 for x in range(12)]
    arm_out.append(0)
    drive_out = [0, 0, 0]

    # Drive
    if joy_inp_axes[0] > 0:
        # Anticlockwise
        drive_out[0] = 2
        drive_out[1] = int(abs(joy_inp_axes[0]*120))
    elif joy_inp_axes[0] < 0:
        # Clockwise
        drive_out[0] = 4
        drive_out[1] = int(abs(joy_inp_axes[0]*120))
    elif joy_inp_axes[1] > 0:
        # Forward
        drive_out[0] = 1
        drive_out[1] = int(abs(joy_inp_axes[1]*120))
    elif joy_inp_axes[1] < 0:
        # Backward
        drive_out[0] = 3
        drive_out[1] = int(abs(joy_inp_axes[1]*120))
    else:
        # Rest
        drive_out[0] = 0
        drive_out[1] = 0

    # Arm

    # ShoulderActuator
    if joy_inp_axes[7] == 1:
        arm_out[0] = 1
    elif joy_inp_axes[7] == -1:
        arm_out[0] = -1
    else:
        arm_out[0] = 0

    # ElbowActuator
    if joy_inp_axes[6] == 1:
        arm_out[2] = 1
    elif joy_inp_axes[6] == -1:
        arm_out[2] = -1
    else:
        arm_out[2] = 0

    # Wrist Actuator
    if joy_inp_buttons[0] == 1:
        arm_out[4] = 1
    elif joy_inp_buttons[3] == 1:
        arm_out[4] = -1
    else:
        arm_out[4] = 0

    # Finger Actuator
    if joy_inp_buttons[1] == 1:
        arm_out[6] = 1
    elif joy_inp_buttons[2] == 1:
        arm_out[6] = -1
    else:
        arm_out[6] = 0

    # Base Rotation
    if joy_inp_axes[2] == -1:
        arm_out[8] = 1
    elif joy_inp_axes[5] == -1:
        arm_out[8] = -1
    else:
        arm_out[8] = 0

    # Gripper Motor
    if joy_inp_buttons[4] == 1:
        arm_out[10] = 1
    elif joy_inp_buttons[5] == 1:
        arm_out[10] = -1
    else:
        arm_out[10] = 0

    arm_out_msg, drive_out_msg = Float64MultiArray(), Float64MultiArray()
    arm_out_msg.data, drive_out_msg.data = arm_out, drive_out
    arm_pub.publish(arm_out_msg)
    drive_pub.publish(drive_out_msg)


if __name__ == '__main__':
    rospy.init_node("basestation_joystick")
    rospy.loginfo("Starting Base Station Joystick Node")
    rospy.Subscriber("/joy", Joy, joy_callback)
    rospy.spin()
