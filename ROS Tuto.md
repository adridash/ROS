ROS Tutorial

How to know the ROS version installed :
rosversion -d
$ -melodic

Prerequisites
For this tutorial we will inspect a package in ros-tutorials, please install it using 
sudo apt-get install ros-melodic-ros-tutorials

Find a package :
rospack find roscpp

Roscd is part of the rosbash suite. It allows you to change directory : 
roscd roscpp

roscd log will take you to the folder where ROS stores log files

rosls allows you to ls directly in a package by name rather than by absolute path. 
Ex : rosls roscpp_tutorials

