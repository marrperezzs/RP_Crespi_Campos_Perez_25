
(cl:in-package :asdf)

(defsystem "ros_game_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "user_msg" :depends-on ("_package_user_msg"))
    (:file "_package_user_msg" :depends-on ("_package"))
  ))