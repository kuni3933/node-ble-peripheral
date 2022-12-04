import bleno from "@abandonware/bleno";
import { EchoCharacteristic } from "./characteristic.js";
import { getSerialNumber } from "raspi-serial-number";

const BlenoPrimaryService = bleno.PrimaryService;

const raspPiSerialNumber = await getSerialNumber()
  .then((number) => {
    return number;
  })
  .catch((error) => {
    console.log(error);
  });

const deviceName = "BerryLock_" + raspPiSerialNumber;
process.env["BLENO_DEVICE_NAME"] = deviceName;

console.log("bleno - echo");
console.log("------------------------------");
console.log("SerialNumber: " + raspPiSerialNumber);
console.log("Initialize_BLE: " + deviceName);
console.log("------------------------------\n");

bleno.on("stateChange", (state) => {
  console.log("on -> stateChange: " + state);

  if (state === "poweredOn") {
    bleno.startAdvertising("echo", ["ec00"], (error) => {
      if (error) {
        console.log(error);
      }
    });
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on("advertisingStart", (error) => {
  console.log(
    "on -> advertisingStart: " + (error ? "error " + error : "success")
  );

  if (!error) {
    bleno.setServices([
      new BlenoPrimaryService({
        uuid: "ec00",
        characteristics: [new EchoCharacteristic()],
      }),
    ]);
  } else {
    console.log(error);
  }
});
