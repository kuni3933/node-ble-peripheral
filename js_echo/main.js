const bleno = require("@abandonware/bleno");
const rsn = require("raspi-serial-number");
const EchoService = require("./service");

raspPiSerialNumber = rsn.getSerialNumberSync((error, data) => {
  if (error) {
    console.log("Callback error: ", error);
    return "Error";
  } else {
    console.log("Callback result: ", data);
    return data;
  }
});
deviceName = "BerryLock_" + raspPiSerialNumber;
process.env["BLENO_DEVICE_NAME"] = deviceName;

console.log("bleno - echo");
console.log("------------------------------");
console.log("SerialNumber: " + raspPiSerialNumber);
console.log("Initialize: " + deviceName);
console.log("------------------------------\n");

bleno.on("stateChange", function (state) {
  console.log("on -> stateChange: " + state);

  if (state === "poweredOn") {
    bleno.startAdvertising(deviceName, ["ec00"]);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on("advertisingStart", function (error) {
  console.log(
    "on -> advertisingStart: " + (error ? "error " + error : "success")
  );

  if (!error) {
    bleno.setServices([new EchoService()]);
  }
});
