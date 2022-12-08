import bleno from "@abandonware/bleno";
import { EchoCharacteristic } from "./characteristic.js";

export class EchoService extends bleno.PrimaryService {
  constructor() {
    super({
      uuid: "ec00",
      characteristics: [new EchoCharacteristic()],
    });
  }
}
