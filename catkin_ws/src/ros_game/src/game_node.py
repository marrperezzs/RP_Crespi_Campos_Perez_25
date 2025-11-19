#!/usr/bin/env python3

import rospy
import time
from ros_game_msgs.msg import user_msg


class GameNode:
    def __init__(self):
        # Create a subscriber to receive user information
        self.sub = rospy.Subscriber('/user_information', user_msg, self.user_info_callback)
        rospy.loginfo("GameNode initialized, waiting for user info...")

    def user_info_callback(self, msg):
        # Log the received user information
        rospy.loginfo("Received user information: Name: %s, Username: %s, Age: %d", msg.name, msg.username, msg.age)
        # Here you can add more game logic based on the received user information
        
if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('game_node')

        # Create an instance of GameNode
        game_node = GameNode()

        rospy.loginfo("GameNode is running. Waiting for user information...")

        # Keep the node running
        rospy.spin()

    except rospy.ROSInterruptException:
        pass

