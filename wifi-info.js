var util = require("util");
var events = require("events");

const fs = require("fs");
const data = JSON.parse(
  fs.readFileSync("/home/pi/Autolock/Wi-fi_Config.json", "utf8")
);

const Wifi = require("rpi-wifi-connection");
const wifi = new Wifi();

function WifiInfo() {
  events.EventEmitter.call(this);
  this.ssid = null;
  this.password = null;
  if ((data.ssid != null || "") && (data.password != null || "")) {
    this.ssid = data.ssid;
    this.password = data.password;
  }
}

util.inherits(WifiInfo, events.EventEmitter);

WifiInfo.prototype.connectCheck = function () {
  var result = null;
  wifi
    .connect({ ssid: this.ssid, psk: this.password })
    .then(() => {
      console.log("Connected to network.");
      result = true;
    })
    .catch((error) => {
      console.log(error);
      result = false;
    });
  this.emit("ready", result);
};

module.exports.WifiInfo = WifiInfo;
