import bleno from "@abandonware/bleno";

const BlenoCharacteristic = bleno.Characteristic;

export class EchoCharacteristic extends BlenoCharacteristic {
  _value;
  _updateValueCallback;

  constructor() {
    super({
      uuid: "ec0e",
      properties: ["read", "write"],
      value: null,
    });
    this._value = Buffer.alloc(0);
    this._updateValueCallback = null;
  }

  onReadRequest(offset, callback) {
    console.log(
      "EchoCharacteristic - onReadRequest: value = " +
        this._value.toString("hex")
    );

    callback(this.RESULT_SUCCESS, this._value);
  }

  onWriteRequest(data, offset, withoutResponse, callback) {
    this._value = data;

    console.log(
      "EchoCharacteristic - onWriteRequest: value = " +
        this._value.toString("hex")
    );

    if (this._updateValueCallback) {
      console.log("EchoCharacteristic - onWriteRequest: notifying");

      this._updateValueCallback(this._value);
    }

    callback(this.RESULT_SUCCESS);
  }
}
