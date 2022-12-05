import bleno from "@abandonware/bleno";

export class EchoCharacteristic extends bleno.Characteristic {
  _value;
  _updateValueCallback;

  constructor() {
    super({
      uuid: "ec0e",
      properties: ["read", "write"],
      value: undefined,
    });
    this._value = Buffer.alloc(0);
  }

  onReadRequest(offset, callback) {
    console.log(
      "EchoCharacteristic - onReadRequest: value = " +
        this._value.toString("hex")
    );
    console.log(
      "EchoCharacteristic - onReadRequest: value = " + this._value + "\n"
    );
    callback(this.RESULT_SUCCESS, this._value);
  }

  onWriteRequest(data, offset, withoutResponse, callback) {
    this._value = data;
    console.log(
      "EchoCharacteristic - onWriteRequest: value = " +
        this._value.toString("hex")
    );
    console.log(
      "EchoCharacteristic - onWriteRequest: value = " + this._value + "\n"
    );
    callback(this.RESULT_SUCCESS);
  }
}
