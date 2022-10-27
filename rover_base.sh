#!/usr/bin/env bash

gnome-terminal --tab --command="roscore"
cd ~/MRT/WorkSpaces/base_ws/
source devel/setup.bash
export ROS_MASTER_URI=http://iitbmartian-H310M-S2:11311/
rover_hostname=MRT-NUC
rover_username=rover
password=2409
gnome-terminal --tab --command="roslaunch basestation joystick_run.launch"
gnome-terminal --tab --command="sshpass -p $password ssh -o StrictHostKeyChecking=no -l $rover_username $rover_hostname 'source ~/ws/rover_ws/src/rover_mobility/rover_drive.sh'"
gnome-terminal --tab --command="sshpass -p $password ssh -o StrictHostKeyChecking=no -l $rover_username $rover_hostname 'source ~/ws/rover_ws/src/rover_mobility/rover_arm.sh'"