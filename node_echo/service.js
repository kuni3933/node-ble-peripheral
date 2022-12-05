import bleno from "@abandonware/bleno";

export default class EchoService extends bleno.PrimaryService {
  constructor() {
    super({
      uuid: "ec00",
      characteristics: [new EchoCharacteristic()],
    });
  }
}
