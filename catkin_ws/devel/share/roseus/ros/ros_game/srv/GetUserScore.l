;; Auto-generated. Do not edit!


(when (boundp 'ros_game::GetUserScore)
  (if (not (find-package "ROS_GAME"))
    (make-package "ROS_GAME"))
  (shadow 'GetUserScore (find-package "ROS_GAME")))
(unless (find-package "ROS_GAME::GETUSERSCORE")
  (make-package "ROS_GAME::GETUSERSCORE"))
(unless (find-package "ROS_GAME::GETUSERSCOREREQUEST")
  (make-package "ROS_GAME::GETUSERSCOREREQUEST"))
(unless (find-package "ROS_GAME::GETUSERSCORERESPONSE")
  (make-package "ROS_GAME::GETUSERSCORERESPONSE"))

(in-package "ROS")





(defclass ros_game::GetUserScoreRequest
  :super ros::object
  :slots (_username ))

(defmethod ros_game::GetUserScoreRequest
  (:init
   (&key
    ((:username __username) "")
    )
   (send-super :init)
   (setq _username (string __username))
   self)
  (:username
   (&optional __username)
   (if __username (setq _username __username)) _username)
  (:serialization-length
   ()
   (+
    ;; string _username
    4 (length _username)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _username
       (write-long (length _username) s) (princ _username s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _username
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _username (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass ros_game::GetUserScoreResponse
  :super ros::object
  :slots (_score ))

(defmethod ros_game::GetUserScoreResponse
  (:init
   (&key
    ((:score __score) 0)
    )
   (send-super :init)
   (setq _score (round __score))
   self)
  (:score
   (&optional __score)
   (if __score (setq _score __score)) _score)
  (:serialization-length
   ()
   (+
    ;; int64 _score
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _score
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _score (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _score) (= (length (_score . bv)) 2)) ;; bignum
              (write-long (ash (elt (_score . bv) 0) 0) s)
              (write-long (ash (elt (_score . bv) 1) -1) s))
             ((and (class _score) (= (length (_score . bv)) 1)) ;; big1
              (write-long (elt (_score . bv) 0) s)
              (write-long (if (>= _score 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _score s)(write-long (if (>= _score 0) 0 #xffffffff) s)))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _score
#+(or :alpha :irix6 :x86_64)
      (setf _score (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _score (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
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

(defclass ros_game::GetUserScore
  :super ros::object
  :slots ())

(setf (get ros_game::GetUserScore :md5sum-) "ce20595763f2770f6e27a12a2546995d")
(setf (get ros_game::GetUserScore :datatype-) "ros_game/GetUserScore")
(setf (get ros_game::GetUserScore :request) ros_game::GetUserScoreRequest)
(setf (get ros_game::GetUserScore :response) ros_game::GetUserScoreResponse)

(defmethod ros_game::GetUserScoreRequest
  (:response () (instance ros_game::GetUserScoreResponse :init)))

(setf (get ros_game::GetUserScoreRequest :md5sum-) "ce20595763f2770f6e27a12a2546995d")
(setf (get ros_game::GetUserScoreRequest :datatype-) "ros_game/GetUserScoreRequest")
(setf (get ros_game::GetUserScoreRequest :definition-)
      "string username
---
int64 score
")

(setf (get ros_game::GetUserScoreResponse :md5sum-) "ce20595763f2770f6e27a12a2546995d")
(setf (get ros_game::GetUserScoreResponse :datatype-) "ros_game/GetUserScoreResponse")
(setf (get ros_game::GetUserScoreResponse :definition-)
      "string username
---
int64 score
")



(provide :ros_game/GetUserScore "ce20595763f2770f6e27a12a2546995d")


