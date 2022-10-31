#!/bin/bash
gnome-terminal --tab -- roscore
cd ~/MRT/Workspaces/base_ws
source devel/setup.bash
echo "Enter Hostname:"
read name
export ROS_MASTER_URI=http://$name:11311/
rover_hostname=rover 
rover_username=MRT-NUC
# echo 'Please enter ROS_MASTER_URI'
# read ROS_MASTER_URI_READ 
# export ROS_MASTER_URI=$ROS_MASTER_URI_READ
# echo 'Please enter rover hostname'
# read rover_hostname
# echo 'Please enter rover username'
# read rover_username
password=2409
gnome-terminal --tab -- roslaunch basestation joystick_run.launch
gnome-terminal --tab -- sshpass -p $password ssh -l $rover_username $rover_hostname 'export ROS_MASTER_URI=http://vedika-ubuntu:11311/;source ~/ws/rover_ws/src/rover-mobility/rover_drive.sh; $SHELL'
gnome-terminal --tab -- sshpass -p $password ssh -l $rover_username $rover_hostname 'export ROS_MASTER_URI=http://vedika-ubuntu:11311/;source ~/ws/rover_ws/src/rover-mobility/rover_arm.sh; $SHELL'
gnome-terminal --tab -- sshpass -p $password ssh -l $rover_username $rover_hostname 'export ROS_MASTER_URI=http://vedika-ubuntu:11311/;source ~/ws/rover_ws/src/rover-mobility/rover_light.sh; $SHELL'
gnome-terminal --tab -- sshpass -p $password ssh -l $rover_username $rover_hostname 'export ROS_MASTER_URI=http://vedika-ubuntu:11311/;source ~/ws/rover_ws/src/rover-mobility/rover_measure.sh; $SHELL'
