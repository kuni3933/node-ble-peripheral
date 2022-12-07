const bleno = require("@abandonware/bleno");
const EchoCharacteristic = require("./characteristic");

const EchoService = function () {
  bleno.PrimaryService.super_.call(this, {
    uuid: "ec00",
    characteristics: [new EchoCharacteristic()],
  });
};

util.inherits(EchoService, bleno.PrimaryService);

module.exports = EchoService;
