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

class SetGameDifficultyRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.change_difficulty = null;
    }
    else {
      if (initObj.hasOwnProperty('change_difficulty')) {
        this.change_difficulty = initObj.change_difficulty
      }
      else {
        this.change_difficulty = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetGameDifficultyRequest
    // Serialize message field [change_difficulty]
    bufferOffset = _serializer.string(obj.change_difficulty, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetGameDifficultyRequest
    let len;
    let data = new SetGameDifficultyRequest(null);
    // Deserialize message field [change_difficulty]
    data.change_difficulty = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.change_difficulty);
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_game/SetGameDifficultyRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b8a8d257ae7cf9a054243931c3dfd215';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string change_difficulty
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetGameDifficultyRequest(null);
    if (msg.change_difficulty !== undefined) {
      resolved.change_difficulty = msg.change_difficulty;
    }
    else {
      resolved.change_difficulty = ''
    }

    return resolved;
    }
};

class SetGameDifficultyResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.success = null;
    }
    else {
      if (initObj.hasOwnProperty('success')) {
        this.success = initObj.success
      }
      else {
        this.success = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetGameDifficultyResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetGameDifficultyResponse
    let len;
    let data = new SetGameDifficultyResponse(null);
    // Deserialize message field [success]
    data.success = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_game/SetGameDifficultyResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '358e233cde0c8a8bcfea4ce193f8fc15';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool success
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetGameDifficultyResponse(null);
    if (msg.success !== undefined) {
      resolved.success = msg.success;
    }
    else {
      resolved.success = false
    }

    return resolved;
    }
};

module.exports = {
  Request: SetGameDifficultyRequest,
  Response: SetGameDifficultyResponse,
  md5sum() { return '9d6c7c12eefb5ab4ae8ce42c4c512e6f'; },
  datatype() { return 'ros_game/SetGameDifficulty'; }
};
