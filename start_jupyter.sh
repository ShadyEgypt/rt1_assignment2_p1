#!/bin/bash

export PYTHONPATH=/root/ros_ws/devel/lib/python3/dist-packages:/opt/ros/noetic/lib/python3/dist-packages:/usr/lib/python3/dist-packages

source /opt/ros/noetic/setup.bash
source /root/ros_ws/devel/setup.bash
python3 -m jupyter notebook --allow-root
