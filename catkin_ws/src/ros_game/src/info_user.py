#!/usr/bin/env python3
import rospy
import time
from ros_game_msgs.msg import user_msg


class InfoUserNode:
    def __init__(self):
        # Create a publisher to publish user information
        self.pub = rospy.Publisher('/user_information', user_msg, queue_size=10)
        rospy.loginfo("InfoUserNode initialized, ready to publish user info.")

        #wait for the publisher to be ready
        #time.sleep(5)

        #call the main function
        self.main()

    def main(self):
        #ask for user input name, username and age
        name = input("Enter your name: ")
        username = input("Enter your username: ")
        age = input("Enter your age: ")

        #create a user_msg message
        user_info = user_msg()
        user_info.name = name
        user_info.username = username
        user_info.age = int(age)

        #publish the user information
        self.pub.publish(user_info)
        rospy.loginfo("Published user information: Name: %s, Username: %s, Age: %d", name, username, int(age))

if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('info_user_node')

        # Create an instance of InfoUserNode
        info_user_node = InfoUserNode()

    except rospy.ROSInterruptException:
        pass

