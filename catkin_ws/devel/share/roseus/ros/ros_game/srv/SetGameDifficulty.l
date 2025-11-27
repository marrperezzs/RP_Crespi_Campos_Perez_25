;; Auto-generated. Do not edit!


(when (boundp 'ros_game::SetGameDifficulty)
  (if (not (find-package "ROS_GAME"))
    (make-package "ROS_GAME"))
  (shadow 'SetGameDifficulty (find-package "ROS_GAME")))
(unless (find-package "ROS_GAME::SETGAMEDIFFICULTY")
  (make-package "ROS_GAME::SETGAMEDIFFICULTY"))
(unless (find-package "ROS_GAME::SETGAMEDIFFICULTYREQUEST")
  (make-package "ROS_GAME::SETGAMEDIFFICULTYREQUEST"))
(unless (find-package "ROS_GAME::SETGAMEDIFFICULTYRESPONSE")
  (make-package "ROS_GAME::SETGAMEDIFFICULTYRESPONSE"))

(in-package "ROS")





(defclass ros_game::SetGameDifficultyRequest
  :super ros::object
  :slots (_change_difficulty ))

(defmethod ros_game::SetGameDifficultyRequest
  (:init
   (&key
    ((:change_difficulty __change_difficulty) "")
    )
   (send-super :init)
   (setq _change_difficulty (string __change_difficulty))
   self)
  (:change_difficulty
   (&optional __change_difficulty)
   (if __change_difficulty (setq _change_difficulty __change_difficulty)) _change_difficulty)
  (:serialization-length
   ()
   (+
    ;; string _change_difficulty
    4 (length _change_difficulty)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _change_difficulty
       (write-long (length _change_difficulty) s) (princ _change_difficulty s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _change_difficulty
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _change_difficulty (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass ros_game::SetGameDifficultyResponse
  :super ros::object
  :slots (_success ))

(defmethod ros_game::SetGameDifficultyResponse
  (:init
   (&key
    ((:success __success) nil)
    )
   (send-super :init)
   (setq _success __success)
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass ros_game::SetGameDifficulty
  :super ros::object
  :slots ())

(setf (get ros_game::SetGameDifficulty :md5sum-) "9d6c7c12eefb5ab4ae8ce42c4c512e6f")
(setf (get ros_game::SetGameDifficulty :datatype-) "ros_game/SetGameDifficulty")
(setf (get ros_game::SetGameDifficulty :request) ros_game::SetGameDifficultyRequest)
(setf (get ros_game::SetGameDifficulty :response) ros_game::SetGameDifficultyResponse)

(defmethod ros_game::SetGameDifficultyRequest
  (:response () (instance ros_game::SetGameDifficultyResponse :init)))

(setf (get ros_game::SetGameDifficultyRequest :md5sum-) "9d6c7c12eefb5ab4ae8ce42c4c512e6f")
(setf (get ros_game::SetGameDifficultyRequest :datatype-) "ros_game/SetGameDifficultyRequest")
(setf (get ros_game::SetGameDifficultyRequest :definition-)
      "string change_difficulty
---
bool success
")

(setf (get ros_game::SetGameDifficultyResponse :md5sum-) "9d6c7c12eefb5ab4ae8ce42c4c512e6f")
(setf (get ros_game::SetGameDifficultyResponse :datatype-) "ros_game/SetGameDifficultyResponse")
(setf (get ros_game::SetGameDifficultyResponse :definition-)
      "string change_difficulty
---
bool success
")



(provide :ros_game/SetGameDifficulty "9d6c7c12eefb5ab4ae8ce42c4c512e6f")


