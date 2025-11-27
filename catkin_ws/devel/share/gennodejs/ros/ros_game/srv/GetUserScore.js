// Auto-generated. Do not edit!

// (in-package ros_game.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class GetUserScoreRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.username = null;
    }
    else {
      if (initObj.hasOwnProperty('username')) {
        this.username = initObj.username
      }
      else {
        this.username = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetUserScoreRequest
    // Serialize message field [username]
    bufferOffset = _serializer.string(obj.username, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetUserScoreRequest
    let len;
    let data = new GetUserScoreRequest(null);
    // Deserialize message field [username]
    data.username = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.username);
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_game/GetUserScoreRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e6839c60033378e900ba73a23bfa5117';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string username
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetUserScoreRequest(null);
    if (msg.username !== undefined) {
      resolved.username = msg.username;
    }
    else {
      resolved.username = ''
    }

    return resolved;
    }
};

class GetUserScoreResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.score = null;
    }
    else {
      if (initObj.hasOwnProperty('score')) {
        this.score = initObj.score
      }
      else {
        this.score = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetUserScoreResponse
    // Serialize message field [score]
    bufferOffset = _serializer.int64(obj.score, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetUserScoreResponse
    let len;
    let data = new GetUserScoreResponse(null);
    // Deserialize message field [score]
    data.score = _deserializer.int64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_game/GetUserScoreResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'eaf3eca167acf95b8816d9344dba8b72';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int64 score
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetUserScoreResponse(null);
    if (msg.score !== undefined) {
      resolved.score = msg.score;
    }
    else {
      resolved.score = 0
    }

    return resolved;
    }
};

module.exports = {
  Request: GetUserScoreRequest,
  Response: GetUserScoreResponse,
  md5sum() { return 'ce20595763f2770f6e27a12a2546995d'; },
  datatype() { return 'ros_game/GetUserScore'; }
};
