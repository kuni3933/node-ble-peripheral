import bleno from "@abandonware/bleno";
import { EchoService } from "./service.js";
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
    bleno.startAdvertising(deviceName, ["ec00"], (error) => {
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
    bleno.setServices([new EchoService()]);
  } else {
    console.log(error);
  }
});

bleno.on("accept", (clientAddress) => {
  log.debug(`ble central connected: ${clientAddress}`);
  bleno.updateRssi();
});

bleno.on("disconnect", (clientAddress) => {
  log.debug(`ble central disconnected: ${clientAddress}`);
});

bleno.on("platform", (event) => {
  log.debug("platform", event);
});

bleno.on("addressChange", (event) => {
  log.debug("addressChange", event);
});

bleno.on("mtuChange", (event) => {
  log.debug("mtuChange", event);
});

bleno.on("advertisingStartError", (event) => {
  log.debug("advertisingStartError", event);
});

bleno.on("servicesSetError", (event) => {
  log.debug("servicesSetError", event);
});

bleno.on("rssiUpdate", (event) => {
  log.debug("rssiUpdate", event);
});
