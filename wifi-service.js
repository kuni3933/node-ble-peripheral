var util = require("util");
var bleno = require("@abandonware/bleno");

var SsidCharacteristic = require("./ssid-characteristic");
var PasswordCharacteristic = require("./password-characteristic");
var ConnectChechCharacteristic = reqire("./connectCheck-characteristic.js");

function WiFi_Service(wifi_info) {
  bleno.PrimaryService.call(this, {
    uuid: "13333333333333333333333333333337",
    characteristics: [
      new SsidCharacteristic(wifi_info),
      new PasswordCharacteristic(wifi_info),
      new ConnectChechCharacteristic(wifi_info),
    ],
  });
}

util.inherits(WiFi_Service, bleno.PrimaryService);

module.exports = WiFi_Service;
