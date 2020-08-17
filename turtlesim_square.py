#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import numpy as np

is_init_pose = False
is_init_degree = False
turnCCW = False

initPose = []
currentPose = []

linearVel = 0.75
angularVel = 0.2

distanceLength = 2.0
angleLength = np.pi/2.0 #change divider 
turn = False
status = ""
save_pose = []
def poseReceived(position_data): #callback
    global currentPose
    currentPose = [position_data.x, position_data.y, position_data.theta]

def moveSquare():

    # anglRadius = (angleDegree * 2 * np.pi)/360

    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, poseReceived)

    turtleVel = Twist()

    rospy.init_node('moveSquare4turtleSim', anonymous=False)
    rate = rospy.Rate(20) # 20hz

    flag = 0


    while not rospy.is_shutdown():

        if flag == 0:
            save_pose = currentPose
            print(save_pose)
            flag = 1
        Dist = np.sqrt(np.power(currentPose[0]-save_pose[0],2) + np.power(currentPose[1]-save_pose[1],2))
        if Dist >= distanceLength:
            turtleVel.linear.x = 0
            if currentPose[2] < 0:
                currentPose[2] = np.abs(currentPose[2]) + np.pi
            if save_pose[2] < 0:
                save_pose[2] = np.abs(save_pose[2]) + np.pi
            angleDist = np.abs(currentPose[2]-save_pose[2])
            if angleDist >= angleLength:
                flag = 0
                turtleVel.linear.x = 0
                turtleVel.angular.z = 0
            else:
                turtleVel.linear.x = 0
                turtleVel.angular.z = angularVel
        else:
            turtleVel.linear.x = linearVel
        velocity_publisher.publish(turtleVel)

        # rospy.loginfo(status)
        rate.sleep()

if __name__ == '__main__':
    try:
        moveSquare()
    except rospy.ROSInterruptException:
        pass
