var util = require("util");
var bleno = require("@abandonware/bleno");
var pizza = require("./wifi-info");

function ConnectChechCharacteristic(wifi_info) {
  bleno.Characteristic.call(this, {
    uuid: "13333333333333333333333333330001",
    properties: ["read"],
    descriptors: [
      new bleno.Descriptor({
        uuid: "2901",
        value: "Gets or sets SSID.",
      }),
    ],
  });

  this.wifi_info = wifi_info;
}

util.inherits(ConnectChechCharacteristic, bleno.Characteristic);

ConnectChechCharacteristic.prototype.onReadRequest = function (
  offset,
  callback
) {
  var result = this.wifi_info.connectCheck();
  console.log("ConnectCheckCharacteristic - onReadRequest:  = " + result);
  callback(
    this.RESULT_SUCCESS,
    result.split("").map((v) => v.charCodeAt(0).toString("hex"))
  );
};

module.exports = ConnectChechCharacteristic;
