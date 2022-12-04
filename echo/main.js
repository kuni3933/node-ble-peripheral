import bleno from "@abandonware/bleno";
import EchoCharacteristic from "./characteristic";
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
print("------------------------------");
print("SerialNumber: " + raspPiSerialNumber);
print("Initialize_BLE: " + deviceName);
print("------------------------------\n");

bleno.on("stateChange", function (state) {
  console.log("on -> stateChange: " + state);

  if (state === "poweredOn") {
    bleno.startAdvertising("echo", ["ec00"]);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on("advertisingStart", function (error) {
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
  }
});
