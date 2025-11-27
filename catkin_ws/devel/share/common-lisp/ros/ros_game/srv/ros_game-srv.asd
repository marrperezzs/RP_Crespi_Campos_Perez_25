
(cl:in-package :asdf)

(defsystem "ros_game-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "GetUserScore" :depends-on ("_package_GetUserScore"))
    (:file "_package_GetUserScore" :depends-on ("_package"))
    (:file "SetGameDifficulty" :depends-on ("_package_SetGameDifficulty"))
    (:file "_package_SetGameDifficulty" :depends-on ("_package"))
  ))