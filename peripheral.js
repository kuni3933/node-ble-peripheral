var util = require("util");
var bleno = require("@abandonware/bleno");

//
// WifiInfo
// * has ssid
// * has password
//
var wifi_info = require("./wifi-info");

//
// The BLE Pizza Service!
//
var WiFi_Service = require("./wifi-service");

//
// A name to advertise our Pizza Service.
//
var name = "Wifi-Settings";
var wifiService = new WiFi_Service(new wifi_info.WifiInfo());

//
// Wait until the BLE radio powers on before attempting to advertise.
// If you don't have a BLE radio, then it will never power on!
//
bleno.on("stateChange", function (state) {
  if (state === "poweredOn") {
    //
    // We will also advertise the service ID in the advertising packet,
    // so it's easier to find.
    //
    bleno.startAdvertising(name, [wifiService.uuid], function (err) {
      if (err) {
        console.log(err);
      }
    });
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on("advertisingStart", function (err) {
  if (!err) {
    console.log("advertising...");
    //
    // Once we are advertising, it's time to set up our services,
    // along with our characteristics.
    //
    bleno.setServices([wifiService]);
  }
});
