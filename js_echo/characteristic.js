const util = require("util");
const bleno = require("@abandonware/bleno");

const EchoCharacteristic = function () {
  EchoCharacteristic.super_.call(this, {
    uuid: "ec0e",
    properties: ["read", "write"],
    value: null,
  });

  this._value = Buffer.alloc(0);
};

util.inherits(EchoCharacteristic, bleno.Characteristic);

EchoCharacteristic.prototype.onReadRequest = function (offset, callback) {
  console.log("EchoCharacteristic - onReadRequest: value = " + this._value);
  console.log(
    "EchoCharacteristic - onReadRequest: value = " + this._value.toString("hex")
  );

  callback(this.RESULT_SUCCESS, this._value);
};

EchoCharacteristic.prototype.onWriteRequest = function (
  data,
  offset,
  withoutResponse,
  callback
) {
  this._value = data;

  console.log("EchoCharacteristic - onWriteRequest: value = " + this._value);
  console.log(
    "EchoCharacteristic - onWriteRequest: value = " +
      this._value.toString("hex")
  );

  callback(this.RESULT_SUCCESS);
};

module.exports = EchoCharacteristic;
