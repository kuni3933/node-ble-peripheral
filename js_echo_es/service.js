import { PrimaryService } from "@abandonware/bleno";
import { EchoCharacteristic } from "./characteristic.js";

export class EchoService extends PrimaryService {
  constructor() {
    super({
      uuid: "ec00",
      characteristics: [new EchoCharacteristic()],
    });
  }
}
