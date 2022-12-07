import { Characteristic } from "@abandonware/bleno";

export class EchoCharacteristic extends Characteristic {
  constructor() {
    super({
      uuid: "ec0e",
      properties: ["read", "write"],
      value: null,
    });
    this._value = Buffer.alloc(0);
  }

  onReadRequest(offset, callback) {
    console.log("EchoCharacteristic - onReadRequest: value = " + this._value);
    console.log(
      "EchoCharacteristic - onReadRequest: value = " +
        this._value.toString("hex") +
        "\n"
    );

    callback(this.RESULT_SUCCESS, this._value);
  }

  onWriteRequest(data, offset, withoutResponse, callback) {
    this._value = data;

    console.log("EchoCharacteristic - onWriteRequest: value = " + this._value);
    console.log(
      "EchoCharacteristic - onWriteRequest: value = " +
        this._value.toString("hex") +
        "\n"
    );

    callback(this.RESULT_SUCCESS);
  }
}