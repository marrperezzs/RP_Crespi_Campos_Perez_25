# RP_Crespi_Campos_Perez_25
# 1. Dependencies

pygame

# 2. How to run

cd catkin_ws
catkin_make
source devel/setup.bash
roslaunch ros_game game_full.launch

# 3. Game dynamic

3 windows will open apart from the normal terminal: the game, a blank pygame screen for the node control and the terminal of the control_node.
You will have to provide your name, username and age in the normal terminal (the name will appear in the game screen). You should do it before playing but can technically do it later.
To start the game click in the game window and push any key to go to the next phase. To control the user click on the blank pygame screen (the control_node) and use the arrow keys to play (space also available to jump)(the arrows of left and right are implemented but don't do anything in the game).
After finishing the game the score will be shown in the screen but will also be shown by result_node in the terminal (only if a user info was recived).
You can retry the game by pushing "R", you will have the same username as before. 

You can change the speed of the game by changing the difficulty with the service implemented. Use another terminal for this.
You can see the user name, the player color and phase using the parameter implemented using the terminal. Player color can also be changed.


# 4. Node-to-node communication

info_user node: collects the user information, publishes it to the /user_information topic in the custom message user_msg dies afert publishing.
control_node : publishes on the topic /keybord_control the command to move the player.
result_node : is subscribed to the topics /user_information and /result_information. when it gets both messages it will ask through the user_score service (as a client) for the percentage score of that user and print it.
    (We implemented also result_game.py as per the part 1 specifications, but we redid it in the result_node.py with services to follow the part 2 specifications)
game_node : this node is subscribed to the topic /keybord_control and uses the recived messages to move the user and to /user_information to print the name of the user in the welcome screen. 
    It is also the publisher of the /result_information topic that sends the score calculated after finishing the game.
    This node is also the server of the services /user_score (that return the percentage score (over the maximum score) of the user given) and /difficulty (that changes the speed of the game and returns True if done correctly)
    This node also has the 3 parameters implemented: user_name, change_player_color and screen_param. These can be accessed through the terminal and changed.
