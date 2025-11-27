; Auto-generated. Do not edit!


(cl:in-package ros_game-srv)


;//! \htmlinclude SetGameDifficulty-request.msg.html

(cl:defclass <SetGameDifficulty-request> (roslisp-msg-protocol:ros-message)
  ((change_difficulty
    :reader change_difficulty
    :initarg :change_difficulty
    :type cl:string
    :initform ""))
)

(cl:defclass SetGameDifficulty-request (<SetGameDifficulty-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetGameDifficulty-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetGameDifficulty-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_game-srv:<SetGameDifficulty-request> is deprecated: use ros_game-srv:SetGameDifficulty-request instead.")))

(cl:ensure-generic-function 'change_difficulty-val :lambda-list '(m))
(cl:defmethod change_difficulty-val ((m <SetGameDifficulty-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_game-srv:change_difficulty-val is deprecated.  Use ros_game-srv:change_difficulty instead.")
  (change_difficulty m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetGameDifficulty-request>) ostream)
  "Serializes a message object of type '<SetGameDifficulty-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'change_difficulty))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'change_difficulty))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetGameDifficulty-request>) istream)
  "Deserializes a message object of type '<SetGameDifficulty-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'change_difficulty) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'change_difficulty) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetGameDifficulty-request>)))
  "Returns string type for a service object of type '<SetGameDifficulty-request>"
  "ros_game/SetGameDifficultyRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetGameDifficulty-request)))
  "Returns string type for a service object of type 'SetGameDifficulty-request"
  "ros_game/SetGameDifficultyRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetGameDifficulty-request>)))
  "Returns md5sum for a message object of type '<SetGameDifficulty-request>"
  "9d6c7c12eefb5ab4ae8ce42c4c512e6f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetGameDifficulty-request)))
  "Returns md5sum for a message object of type 'SetGameDifficulty-request"
  "9d6c7c12eefb5ab4ae8ce42c4c512e6f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetGameDifficulty-request>)))
  "Returns full string definition for message of type '<SetGameDifficulty-request>"
  (cl:format cl:nil "string change_difficulty~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetGameDifficulty-request)))
  "Returns full string definition for message of type 'SetGameDifficulty-request"
  (cl:format cl:nil "string change_difficulty~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetGameDifficulty-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'change_difficulty))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetGameDifficulty-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetGameDifficulty-request
    (cl:cons ':change_difficulty (change_difficulty msg))
))
;//! \htmlinclude SetGameDifficulty-response.msg.html

(cl:defclass <SetGameDifficulty-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass SetGameDifficulty-response (<SetGameDifficulty-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetGameDifficulty-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetGameDifficulty-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_game-srv:<SetGameDifficulty-response> is deprecated: use ros_game-srv:SetGameDifficulty-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <SetGameDifficulty-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_game-srv:success-val is deprecated.  Use ros_game-srv:success instead.")
  (success m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetGameDifficulty-response>) ostream)
  "Serializes a message object of type '<SetGameDifficulty-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetGameDifficulty-response>) istream)
  "Deserializes a message object of type '<SetGameDifficulty-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetGameDifficulty-response>)))
  "Returns string type for a service object of type '<SetGameDifficulty-response>"
  "ros_game/SetGameDifficultyResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetGameDifficulty-response)))
  "Returns string type for a service object of type 'SetGameDifficulty-response"
  "ros_game/SetGameDifficultyResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetGameDifficulty-response>)))
  "Returns md5sum for a message object of type '<SetGameDifficulty-response>"
  "9d6c7c12eefb5ab4ae8ce42c4c512e6f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetGameDifficulty-response)))
  "Returns md5sum for a message object of type 'SetGameDifficulty-response"
  "9d6c7c12eefb5ab4ae8ce42c4c512e6f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetGameDifficulty-response>)))
  "Returns full string definition for message of type '<SetGameDifficulty-response>"
  (cl:format cl:nil "bool success~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetGameDifficulty-response)))
  "Returns full string definition for message of type 'SetGameDifficulty-response"
  (cl:format cl:nil "bool success~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetGameDifficulty-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetGameDifficulty-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetGameDifficulty-response
    (cl:cons ':success (success msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetGameDifficulty)))
  'SetGameDifficulty-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetGameDifficulty)))
  'SetGameDifficulty-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetGameDifficulty)))
  "Returns string type for a service object of type '<SetGameDifficulty>"
  "ros_game/SetGameDifficulty")