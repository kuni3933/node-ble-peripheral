var util = require("util");
var bleno = require("@abandonware/bleno");
var pizza = require("./wifi-info");

function SsidCharacteristic(wifi_info) {
  bleno.Characteristic.call(this, {
    uuid: "13333333333333333333333333330001",
    properties: ["read", "write"],
    descriptors: [
      new bleno.Descriptor({
        uuid: "2901",
        value: "Gets or sets SSID.",
      }),
    ],
  });

  this.wifi_info = wifi_info;
}

util.inherits(SsidCharacteristic, bleno.Characteristic);

SsidCharacteristic.prototype.onReadRequest = function (offset, callback) {
  console.log(
    "SsidCharacteristic - onReadRequest: ssid = " + this.wifi_info.ssid
  );

  callback(
    this.RESULT_SUCCESS,
    this.wifi_info.ssid.split("").map((v) => v.charCodeAt(0).toString("hex"))
  );
};

SsidCharacteristic.prototype.onWriteRequest = function (
  data,
  offset,
  withoutResponse,
  callback
) {
  this.wifi_info.ssid = Buffer.from(data, "hex").toString("utf-8");
  console.log(
    "SsidCharacteristic - onWriteRequest: ssid = " + this.wifi_info.ssid
  );

  callback(this.RESULT_SUCCESS);
};

module.exports = SsidCharacteristic;
