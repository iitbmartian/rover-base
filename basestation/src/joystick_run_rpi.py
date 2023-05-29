#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Joy
from rover_msgs.msg import drive_msg, arm_msg

arm_pub = rospy.Publisher('/rover/arm_rpi_directives', arm_msg, queue_size=1)


def joy_callback(joy_inp):
    joy_inp_axes = joy_inp.axes
    joy_inp_buttons = joy_inp.buttons

    arm_out = arm_msg()
    arm_out.shoulder_actuator.mode = "manual"
    arm_out.elbow_actuator.mode = "manual"
    arm_out.base_motor.mode = "manual"
    arm_out.elbow_motor.mode = "manual"
    arm_out.wrist_actuator.mode = "manual"
    arm_out.gripper.mode = "manual"
    arm_out.gripper_rot.mode = "manual"

    # Arm
    # ShoulderActuator
    arm_out.shoulder_actuator.direction = "stop"
    arm_out.shoulder_actuator.speed = 0

    # Elbow Actuator
    arm_out.elbow_actuator.direction = "stop"
    arm_out.elbow_actuator.speed = 0

    # Base Motors
    arm_out.base_motor.direction = "stop"
    arm_out.base_motor.speed = 0

    # Gripper
    if joy_inp_buttons[2] == 1:
        arm_out.gripper.direction = "forward"
        arm_out.gripper.speed = 120
    elif joy_inp_buttons[1] == 1:
        arm_out.gripper.direction = "backward"
        arm_out.gripper.speed = 120
    else:
        arm_out.gripper.direction = "stop"
        arm_out.gripper.speed = 0

    # Wrist Actuator
    arm_out.wrist_actuator.direction = "stop"
    arm_out.wrist_actuator.speed = 0

    # Gripper Rotation
    if joy_inp_buttons[4] == 1:
        arm_out.gripper_rot.direction = "forward"
        arm_out.gripper_rot.speed = 120
    elif joy_inp_buttons[5] == 1:
        arm_out.gripper_rot.direction = "backward"
        arm_out.gripper_rot.speed = 120
    else:
        arm_out.gripper_rot.direction = "stop"
        arm_out.gripper_rot.speed = 0
    
    #Soil Box
    if joy_inp_axes[6] == 1:
        arm_out.soil_box.direction = "forward"
        arm_out.soil_box.speed = 120
    elif joy_inp_axes[6] == -1:
        arm_out.soil_box.direction = "backward"
        arm_out.soil_box.speed = 120
    else:
        arm_out.soil_box.direction = "stop"
        arm_out.soil_box.speed = 0

    # Elbow Motor
    arm_out.elbow_motor.direction = "stop"
    arm_out.elbow_motor.speed = 0

    # Bio Task
    if joy_inp_buttons[7] == 1:
        arm_out.bio = 'y'
    else:
        arm_out.bio = 'n'

    arm_pub.publish(arm_out)


if __name__ == '__main__':
    rospy.init_node("basestation_joystick_rpi")
    rospy.loginfo("Starting Base Station Joystick Node")
    rospy.Subscriber("/joy", Joy, joy_callback)
    rospy.spin()
