; Auto-generated. Do not edit!


(cl:in-package ros_game-srv)


;//! \htmlinclude GetUserScore-request.msg.html

(cl:defclass <GetUserScore-request> (roslisp-msg-protocol:ros-message)
  ((username
    :reader username
    :initarg :username
    :type cl:string
    :initform ""))
)

(cl:defclass GetUserScore-request (<GetUserScore-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetUserScore-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetUserScore-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_game-srv:<GetUserScore-request> is deprecated: use ros_game-srv:GetUserScore-request instead.")))

(cl:ensure-generic-function 'username-val :lambda-list '(m))
(cl:defmethod username-val ((m <GetUserScore-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_game-srv:username-val is deprecated.  Use ros_game-srv:username instead.")
  (username m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetUserScore-request>) ostream)
  "Serializes a message object of type '<GetUserScore-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'username))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'username))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetUserScore-request>) istream)
  "Deserializes a message object of type '<GetUserScore-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'username) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'username) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetUserScore-request>)))
  "Returns string type for a service object of type '<GetUserScore-request>"
  "ros_game/GetUserScoreRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetUserScore-request)))
  "Returns string type for a service object of type 'GetUserScore-request"
  "ros_game/GetUserScoreRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetUserScore-request>)))
  "Returns md5sum for a message object of type '<GetUserScore-request>"
  "ce20595763f2770f6e27a12a2546995d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetUserScore-request)))
  "Returns md5sum for a message object of type 'GetUserScore-request"
  "ce20595763f2770f6e27a12a2546995d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetUserScore-request>)))
  "Returns full string definition for message of type '<GetUserScore-request>"
  (cl:format cl:nil "string username~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetUserScore-request)))
  "Returns full string definition for message of type 'GetUserScore-request"
  (cl:format cl:nil "string username~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetUserScore-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'username))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetUserScore-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetUserScore-request
    (cl:cons ':username (username msg))
))
;//! \htmlinclude GetUserScore-response.msg.html

(cl:defclass <GetUserScore-response> (roslisp-msg-protocol:ros-message)
  ((score
    :reader score
    :initarg :score
    :type cl:integer
    :initform 0))
)

(cl:defclass GetUserScore-response (<GetUserScore-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetUserScore-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetUserScore-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_game-srv:<GetUserScore-response> is deprecated: use ros_game-srv:GetUserScore-response instead.")))

(cl:ensure-generic-function 'score-val :lambda-list '(m))
(cl:defmethod score-val ((m <GetUserScore-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_game-srv:score-val is deprecated.  Use ros_game-srv:score instead.")
  (score m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetUserScore-response>) ostream)
  "Serializes a message object of type '<GetUserScore-response>"
  (cl:let* ((signed (cl:slot-value msg 'score)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetUserScore-response>) istream)
  "Deserializes a message object of type '<GetUserScore-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'score) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetUserScore-response>)))
  "Returns string type for a service object of type '<GetUserScore-response>"
  "ros_game/GetUserScoreResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetUserScore-response)))
  "Returns string type for a service object of type 'GetUserScore-response"
  "ros_game/GetUserScoreResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetUserScore-response>)))
  "Returns md5sum for a message object of type '<GetUserScore-response>"
  "ce20595763f2770f6e27a12a2546995d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetUserScore-response)))
  "Returns md5sum for a message object of type 'GetUserScore-response"
  "ce20595763f2770f6e27a12a2546995d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetUserScore-response>)))
  "Returns full string definition for message of type '<GetUserScore-response>"
  (cl:format cl:nil "int64 score~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetUserScore-response)))
  "Returns full string definition for message of type 'GetUserScore-response"
  (cl:format cl:nil "int64 score~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetUserScore-response>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetUserScore-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetUserScore-response
    (cl:cons ':score (score msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetUserScore)))
  'GetUserScore-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetUserScore)))
  'GetUserScore-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetUserScore)))
  "Returns string type for a service object of type '<GetUserScore>"
  "ros_game/GetUserScore")