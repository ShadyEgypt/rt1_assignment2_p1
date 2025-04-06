#!/bin/bash

export PYTHONPATH=/home/shady/Documents/unige_robotics_msc/0x02_second_year_2nd_semster/rt2/rt_ros_ws/devel/lib/python3/dist-packages:/opt/ros/noetic/lib/python3/dist-packages:/usr/lib/python3/dist-packages

source /opt/ros/noetic/setup.bash
source /home/shady/Documents/unige_robotics_msc/0x02_second_year_2nd_semster/rt2/rt_ros_ws/devel/setup.bash
jupyter nbextension enable --py widgetsnbextension --user
jupyter notebook
