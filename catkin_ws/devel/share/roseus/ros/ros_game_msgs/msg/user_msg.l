;; Auto-generated. Do not edit!


(when (boundp 'ros_game_msgs::user_msg)
  (if (not (find-package "ROS_GAME_MSGS"))
    (make-package "ROS_GAME_MSGS"))
  (shadow 'user_msg (find-package "ROS_GAME_MSGS")))
(unless (find-package "ROS_GAME_MSGS::USER_MSG")
  (make-package "ROS_GAME_MSGS::USER_MSG"))

(in-package "ROS")
;;//! \htmlinclude user_msg.msg.html


(defclass ros_game_msgs::user_msg
  :super ros::object
  :slots (_name _username _age ))

(defmethod ros_game_msgs::user_msg
  (:init
   (&key
    ((:name __name) "")
    ((:username __username) "")
    ((:age __age) 0)
    )
   (send-super :init)
   (setq _name (string __name))
   (setq _username (string __username))
   (setq _age (round __age))
   self)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:username
   (&optional __username)
   (if __username (setq _username __username)) _username)
  (:age
   (&optional __age)
   (if __age (setq _age __age)) _age)
  (:serialization-length
   ()
   (+
    ;; string _name
    4 (length _name)
    ;; string _username
    4 (length _username)
    ;; int64 _age
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; string _username
       (write-long (length _username) s) (princ _username s)
     ;; int64 _age
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _age (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _age) (= (length (_age . bv)) 2)) ;; bignum
              (write-long (ash (elt (_age . bv) 0) 0) s)
              (write-long (ash (elt (_age . bv) 1) -1) s))
             ((and (class _age) (= (length (_age . bv)) 1)) ;; big1
              (write-long (elt (_age . bv) 0) s)
              (write-long (if (>= _age 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _age s)(write-long (if (>= _age 0) 0 #xffffffff) s)))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _username
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _username (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int64 _age
#+(or :alpha :irix6 :x86_64)
      (setf _age (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _age (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;;
   self)
  )

(setf (get ros_game_msgs::user_msg :md5sum-) "76ad7cc8793d3811f3fd0e458252b5c3")
(setf (get ros_game_msgs::user_msg :datatype-) "ros_game_msgs/user_msg")
(setf (get ros_game_msgs::user_msg :definition-)
      "string name
string username
int64 age
")



(provide :ros_game_msgs/user_msg "76ad7cc8793d3811f3fd0e458252b5c3")


