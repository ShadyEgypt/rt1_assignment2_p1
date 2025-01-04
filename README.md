# Research Track 1 - Assignment 2 part 1

This documentation describes two ROS nodes: `action_client_node.py` and `last_target_service.py`, which work together to handle robot movement goals and track the last target coordinates.

---

## **1. action_client_node.py**

### **Overview**  
The `action_client_node.py` acts as an Action Client that communicates with an Action Server to set and monitor robot movement goals. It also handles robot status and feedback updates and interacts with a service to get or set the last goal coordinates.

### **Subscribed Topics**  
- `/odom` (`nav_msgs/Odometry`): Subscribes to robot odometry data to track position and velocity.

### **Published Topics**  
- `/robot_status` (`rt1_assignment2_p1/RobotStatus`): Publishes robot status including position and velocity.

### **Service Clients**  
- `/get_last_target` (`rt1_assignment2_p1/GetLastTarget`): Used to get or set the last target coordinates.

### **Action Client**  
- `/reaching_goal` (`assignment_2_2024/PlanningAction`): Sends movement goals to the robot.

### **Key Functionalities**  
- **Send Goal:** Set a new target (x, y) for the robot.  
- **Cancel Goal:** Cancel an ongoing movement goal.  
- **Monitor Feedback:** Retrieve real-time feedback from the action server.  
- **Get Status:** Check if a goal is active and its status.  
- **Get Last Target:** Retrieve the last target coordinates via a service call.  
- **Set Last Target:** Update the last target coordinates via a service call.

### **Commands**  
When running the node, you can input the following commands:  
- `set`: Set a new goal with x and y coordinates.  
- `cancel`: Cancel the current goal.  
- `status`: Check the status of the current goal.  
- `feedback`: Retrieve the current position feedback.  
- `last`: Retrieve the last target coordinates.  
- `exit`: Exit the program.

---

## **2. last_target_service.py**

### **Overview**  
The `last_target_service.py` node provides a ROS Service to get or set the last goal coordinates of the robot. It acts as a backend service to persist target coordinates.

### **Service Server**  
- `/get_last_target` (`rt1_assignment2_p1/GetLastTarget`): Provides two functionalities:  
  - **Set Last Target:** Update the last known target (x, y).  
  - **Get Last Target:** Retrieve the last known target (x, y).  

### **Service Definition**  

GetLastTarget.srv \
`bool set_target`:  True to set new target, False to get last target \
`float64 x`:  x-coordinate (if setting target) \
`float64 y`:  y-coordinate (if setting target)\
`float64 res_x`:  Retrieved x-coordinate \
`float64 res_y`:  Retrieved y-coordinate \
`bool success`:  True if operation was successful

### **Key Functionalities**  
- **Set Last Target:** Updates the `last_target` dictionary with new x and y coordinates.  
- **Get Last Target:** Returns the previously set x and y coordinates.

---

## **3. Workflow Between Nodes**

1. `action_client_node` sends movement goals via the Action Server `/reaching_goal`.  
2. Real-time feedback and status are published to `/robot_status`.  
3. If a goal is set, the coordinates are stored in the `last_target_service` node using the `/get_last_target` service.  
4. The `last_target_service` provides stored target coordinates upon request from the client node.

## Launch File
To launch the node, the following launch file was created (`rt1_assignment2_p1.launch`):
This launch file launches the assignment_2_2024 package which is a dependency for this node to run correctly.

### Launch Command
Run the launch file with:
```bash
roslaunch rt1_rt1_assignment2_p1 rt1_assignment2_p1.launch
```
If this command didn't work as expected, then you need to run:
```bash
cd src/rt1_rt1_assignment2_p1/launch
roslaunch rt1_assignment2_p1.launch
```
## Common Errors & Solutions

### Error: robot failed to detect obstacles.
- **Issue:** The issue was that the laser plugin was not working as expected. I investigated with Rviz and noticed no red dots around the robot. 
- **Solution:** I went back to the robot_description package and noticed there's a branch called noetic-laser, I replaced the laser plugin in the assignment_2_2024 package with the laser plugin from the robot_description package, laser-noetic branch, and the issue was solved.

  
## Author
- **Shady Abdelmalek**