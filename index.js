import { fileURLToPath } from "url";
import fs from "fs";
import path from "path";
import rpi_wifi_connection from "rpi-wifi-connection";

class wifi {
  //* プロパティ
  __dirname;
  configDirPath;
  wifi;

  //* コンストラクタ
  constructor() {
    //* wifiインスタンスを生成
    this.wifi = new rpi_wifi_connection();

    //* Configディレクトリのパス
    this.__dirname = path.dirname(fileURLToPath(import.meta.url));
    this.configDirPath = `${this.__dirname}/../Config`;
    //console.log(`configDirPath: ${this.configDirPath}`);
  }

  //* メソッド
  getStatus() {
    this.wifi
      .getStatus()
      .then((status) => {
        if (status.ssid) {
          status.isConnect = true;
        } else {
          status.isConnect = false;
        }
        console.log(JSON.stringify(status));
      })
      .catch((error) => {
        console.log('{ "isConnect": false }');
        //console.log(error);
      });
  }

  connect(ssid, pass) {
    this.wifi
      .connect({ ssid: ssid, psk: pass, timeout: 7500 })
      .then(() => {
        //* ファイル書込
        fs.writeFileSync(
          `${this.configDirPath}/Wifi.json`,
          `{ "ssid": "${ssid}","pass": "${pass}" }`
        );

        //* リターンログ
        console.log('{ "isConnect": true }');
      })
      .catch((error) => {
        console.log('{ "isConnect": false }');
        //console.log(error);
      });
  }

  connectFromJson() {
    //* ファイル読込
    const isJsonExists = fs.existsSync(`${this.configDirPath}/Wifi.json`);

    let json = undefined;
    if (isJsonExists) {
      json = JSON.parse(
        fs.readFileSync(`${this.configDirPath}/Wifi.json`, "utf-8")
      );
    }

    if (json != undefined && json.ssid && json.pass) {
      this.wifi
        .connect({ ssid: json.ssid, psk: json.pass, timeout: 7500 })
        .then(() => {
          //* リターンログ
          console.log('{ "isSConnect": true }');
        })
        .catch((error) => {
          console.log('{ "isConnect": false }');
          //console.log(error);
        });
    } else {
      console.log('{ "isConnect": false }');
    }
  }
}

wifi = new wifi();
//* getStatusを叩かれた場合
if (process.argv.length == 3 && process.argv[2] == "getStatus") {
  wifi.getStatus();
}

//* connectを叩かれた場合
if (process.argv.length == 5 && process.argv[2] == "connect") {
  wifi.connect(process.argv[3], process.argv[4]);
}

//* getStatusを叩かれた場合
if (process.argv.length == 3 && process.argv[2] == "connectFromJson") {
  wifi.connectFromJson();
}
