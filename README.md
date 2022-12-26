# Documentation for Base-Station Setup

## Setting up SSH

* Connect the base-station via wired network (LAN) to the Ruckus or connect wirelessly to Rover-LAN (password: rover2409)
* Setup the IP Address as 192.168.2.x and Netmask as 255.255.255.0
* Add it to `/etc/hosts` file for hostname resolution (required for ROS setup)
* Add the IP Address of NUC as well (192.168.2.2 MRT-NUC)
* Reboot the base-station
* Connect remotely via the command: `ssh rover@MRT-NUC`, password is: 2409

List of IP Addresses in the `/etc/hosts` file:

| Hostname | IP | Description (Ubuntu Version) |
| --- | --- | --- |
| MRT-NUC | 192.168.2.2 | Rover |
| iitbmartian-H310M-S2 | 192.168.2.3 | LabPC(20.04) |
| Pijames-ASUS | 192.168.2.4 | Annirudh Lappy - basestation |
| lenovo | 192.168.2.5 | Khush Lappy - basestation |
| Predator | 192.168.2.6 | Harsh Lappy - basestation |
| vedika-ubuntu | 192.168.2.7 | Vedika Lappy - basestation |
| nishant | 192.168.2.8 | Nishant Lappy - basestation |

## Creating Workspace

* Create a new directory `base_ws`, create directory `src`, and run `catkin_make`
* Git pull `rover-base` in src, and `catkin_make`

## [Configuring Joystick](http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick)
![Joystick_Mapping](https://user-images.githubusercontent.com/99526193/203838436-4851d851-5d19-49b1-bad6-4e7ecf908092.jpg)

## Running the Rover

* Run `roscore` on base-station, and note the ROS-MASTER-URI
* Go into the base_ws and `source devel/setup.bash`, `roslaunch basestation joystick_run.launch`
* Connect remotely via the command: `ssh rover@MRT-NUC`, password is: 2409
* Run the following commands in sequential order on the NUC:
  * `master <hostname>`
  * `cd ~/ws/rover_ws`
  * `.-ws`
  * | Package | Command |
    | --- | --- |
    | Drive | `roslaunch rover_drive drive.launch` |
    | Arm | `roslaunch rover_arm arm.launch` |
    | Light | `roslaunch rover_light light.launch` |
    | Measure | `roslaunch rover_measure measure.launch` |


