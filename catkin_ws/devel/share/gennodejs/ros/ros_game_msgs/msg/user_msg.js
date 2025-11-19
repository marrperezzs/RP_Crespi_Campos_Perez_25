// Auto-generated. Do not edit!

// (in-package ros_game_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class user_msg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.name = null;
      this.username = null;
      this.age = null;
    }
    else {
      if (initObj.hasOwnProperty('name')) {
        this.name = initObj.name
      }
      else {
        this.name = '';
      }
      if (initObj.hasOwnProperty('username')) {
        this.username = initObj.username
      }
      else {
        this.username = '';
      }
      if (initObj.hasOwnProperty('age')) {
        this.age = initObj.age
      }
      else {
        this.age = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type user_msg
    // Serialize message field [name]
    bufferOffset = _serializer.string(obj.name, buffer, bufferOffset);
    // Serialize message field [username]
    bufferOffset = _serializer.string(obj.username, buffer, bufferOffset);
    // Serialize message field [age]
    bufferOffset = _serializer.int64(obj.age, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type user_msg
    let len;
    let data = new user_msg(null);
    // Deserialize message field [name]
    data.name = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [username]
    data.username = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [age]
    data.age = _deserializer.int64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.name);
    length += _getByteLength(object.username);
    return length + 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_game_msgs/user_msg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '76ad7cc8793d3811f3fd0e458252b5c3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string name
    string username
    int64 age
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new user_msg(null);
    if (msg.name !== undefined) {
      resolved.name = msg.name;
    }
    else {
      resolved.name = ''
    }

    if (msg.username !== undefined) {
      resolved.username = msg.username;
    }
    else {
      resolved.username = ''
    }

    if (msg.age !== undefined) {
      resolved.age = msg.age;
    }
    else {
      resolved.age = 0
    }

    return resolved;
    }
};

module.exports = user_msg;
