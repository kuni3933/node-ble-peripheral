var util = require("util");
var bleno = require("@abandonware/bleno");
var pizza = require("./wifi-info");

function PasswordCharacteristic(wifi_info) {
  bleno.Characteristic.call(this, {
    uuid: "13333333333333333333333333330002",
    properties: ["write"],
    descriptors: [
      new bleno.Descriptor({
        uuid: "2901",
        value: "Sets Password.",
      }),
    ],
  });

  this.wifi_info = wifi_info;
}

util.inherits(PasswordCharacteristic, bleno.Characteristic);

PasswordCharacteristic.prototype.onWriteRequest = function (
  data,
  offset,
  withoutResponse,
  callback
) {
  this.wifi_info.password = data;
  console.log(
    "EchoCharacteristic - onReadRequest: password = " +
      this.wifi_info.password.toString("hex").toString("utf-8")
  );

  callback(this.RESULT_SUCCESS);
};

module.exports = PasswordCharacteristic;
