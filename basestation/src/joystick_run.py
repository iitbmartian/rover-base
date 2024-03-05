#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Joy
from rover_msgs.msg import drive_msg, arm_msg

arm_pub = rospy.Publisher('/rover/arm_directives', arm_msg, queue_size=1)
drive_pub = rospy.Publisher('/rover/drive_directives/manual', drive_msg, queue_size=1)


def joy_callback(joy_inp):
    joy_inp_axes = joy_inp.axes
    joy_inp_buttons = joy_inp.buttons

    arm_out = arm_msg()
    drive_out = drive_msg()
    drive_out.mode = "manual"
    arm_out.shoulder_actuator.mode = "manual"
    arm_out.elbow_actuator.mode = "manual"
    arm_out.base_motor.mode = "manual"
    arm_out.elbow_motor.mode = "manual"
    arm_out.wrist_actuator.mode = "manual"
    arm_out.gripper.mode = "manual"
    arm_out.gripper_rot.mode = "manual"

    # Drive
    if joy_inp_axes[0] > 25/120:
        # Anticlockwise
        drive_out.direction = "anticlockwise"
        drive_out.speed = int(abs(joy_inp_axes[0]*120))
    elif joy_inp_axes[0] < -25/120:
        # Clockwise
        drive_out.direction = "clockwise"
        drive_out.speed = int(abs(joy_inp_axes[0]*120))
    elif joy_inp_axes[1] > 25/120:
        # Forward
        drive_out.direction = "forward"
        drive_out.speed = int(abs(joy_inp_axes[1]*120))
    elif joy_inp_axes[1] < -25/120:
        # Backward
        drive_out.direction = "backward"
        drive_out.speed = int(abs(joy_inp_axes[1]*120))
    else:
        # Rest
        drive_out.direction = "stop"
        drive_out.speed = 0

    # Arm
    # ShoulderActuator
    if joy_inp_axes[4] > 25/120:
        arm_out.shoulder_actuator.direction = "backward"
        arm_out.shoulder_actuator.speed = int(abs(joy_inp_axes[4]*120))
    elif joy_inp_axes[4] < -25/120:
        arm_out.shoulder_actuator.direction = "forward"
        arm_out.shoulder_actuator.speed = int(abs(joy_inp_axes[4] * 120))
    else:
        arm_out.shoulder_actuator.direction = "stop"
        arm_out.shoulder_actuator.speed = 0

    # Elbow Actuator
    if joy_inp_axes[7] < -25/120:
        arm_out.elbow_actuator.direction = "forward"
        arm_out.elbow_actuator.speed = int(abs(joy_inp_axes[7]*120))
    elif joy_inp_axes[7] > 25/120:
        arm_out.elbow_actuator.direction = "backward"
        arm_out.elbow_actuator.speed = int(abs(joy_inp_axes[7] * 120))
    else:
        arm_out.elbow_actuator.direction = "stop"
        arm_out.elbow_actuator.speed = 0
    # if (joy_inp_axes[5] < 0.65) or (joy_inp_axes[7] < -25/120):
    #     arm_out.elbow_actuator.direction = "forward"
    #     arm_out.elbow_actuator.speed = max(int(abs(joy_inp_axes[7]*120)), int(abs((joy_inp_axes[5]-1)*60)))
    # elif (joy_inp_axes[2] < 0.65) or (joy_inp_axes[7] > 25/120):
    #     arm_out.elbow_actuator.direction = "backward"
    #     arm_out.elbow_actuator.speed = max(int(abs(joy_inp_axes[7] * 120)), int(abs((joy_inp_axes[2]-1)*60)))
    # else:
    #     arm_out.elbow_actuator.direction = "stop"
    #     arm_out.elbow_actuator.speed = 0

    # Base Motors
    if joy_inp_axes[3] < -25/120:
        arm_out.base_motor.direction = "forward"
        arm_out.base_motor.speed = int(abs(joy_inp_axes[3]*120))
    elif joy_inp_axes[3] > 25/120:
        arm_out.base_motor.direction = "backward"
        arm_out.base_motor.speed = int(abs(joy_inp_axes[3]*120))
    else:
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
    if joy_inp_buttons[3] == 1:
        arm_out.wrist_actuator.direction = "backward"
        arm_out.wrist_actuator.speed = 120
    elif joy_inp_buttons[0] == 1:
        arm_out.wrist_actuator.direction = "forward"
        arm_out.wrist_actuator.speed = 120
    else:
        arm_out.wrist_actuator.direction = "stop"
        arm_out.wrist_actuator.speed = 0

    # Gripper Rotation
    if joy_inp_buttons[4] == 1:
        arm_out.gripper_rot.direction = "backward"
        arm_out.gripper_rot.speed = 120
    elif joy_inp_buttons[5] == 1:
        arm_out.gripper_rot.direction = "forward"
        arm_out.gripper_rot.speed = 120
    else:
        arm_out.gripper_rot.direction = "stop"
        arm_out.gripper_rot.speed = 0

    # Elbow Motor
    if (joy_inp_axes[5] < 0) or (joy_inp_axes[6] < -25/120):
        arm_out.elbow_motor.direction = "backward"
        arm_out.elbow_motor.speed = int(abs(joy_inp_axes[2]*120))
    elif (joy_inp_axes[2] < 0) or (joy_inp_axes[6] > 25/120):
        arm_out.elbow_motor.direction = "forward"
        arm_out.elbow_motor.speed = int(abs(joy_inp_axes[5]*120))
    else:
        arm_out.elbow_motor.direction = "stop"
        arm_out.elbow_motor.speed = 0


    arm_pub.publish(arm_out)
    drive_pub.publish(drive_out)


if __name__ == '__main__':
    rospy.init_node("basestation_joystick")
    rospy.loginfo("Starting Base Station Joystick Node")
    rospy.Subscriber("/joy", Joy, joy_callback)
    rospy.spin()
