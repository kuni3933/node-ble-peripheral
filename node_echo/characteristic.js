import bleno from "@abandonware/bleno";

export class EchoCharacteristic extends bleno.Characteristic {
  _value;
  _updateValueCallback;

  constructor() {
    super({
      uuid: "ec0e",
      properties: ["read", "write"],
      value: null,
    });
    this._value = undefined;
    this._updateValueCallback = undefined;
  }

  onReadRequest(callback) {
    console.log(
      "EchoCharacteristic - onReadRequest: value = " +
        this._value.toString("hex")
    );
    callback(this.RESULT_SUCCESS, this._value);
  }
  onWriteRequest(data, callback) {
    this._value = data;
    console.log(
      "EchoCharacteristic - onWriteRequest: value = " +
        this._value.toString("hex")
    );
    callback(this.RESULT_SUCCESS);
  }
}
