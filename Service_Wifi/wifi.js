import { fileURLToPath } from "url";
import fs from "fs";
import path from "path";
import rpi_wifi_connection from "rpi-wifi-connection";

class wifi {
  //* プロパティ
  configDirPath;
  wifi;

  //* コンストラクタ
  constructor() {
    //* wifiインスタンスを生成
    this.wifi = new rpi_wifi_connection();

    //* Configディレクトリのパス
    this.configDirPath = `${path.dirname(
      fileURLToPath(import.meta.url)
    )}/../../Config`;
    //console.log(`configDirPath: ${this.configDirPath}`);
  }

  //* メソッド
  getStatus() {
    this.wifi
      .getStatus()
      .then((status) => {
        if (status.ssid != undefined) {
          status["isConnect"] = true;
        } else {
          status["isConnect"] = false;
        }
        console.log(JSON.stringify(status));
      })
      .catch((error) => {
        console.log('{ "isConnect": false }');
        console.error(error);
      });
  }

  connect(json) {
    // コマンドライン引数からjsonをパース
    const jsonDecode = () => {
      try {
        return JSON.parse(json);
      } catch (error) {
        console.error(error);
        return undefined;
      }
    };
    // リターンログ用オブジェクト(初期値:false)
    let returnLog = { isConnect: false };

    // 正常にjsonをパース出来ていた場合はconnect
    if (jsonDecode["ssid"] != undefined && jsonDecode["pass"] != undefined) {
      this.wifi
        .connect({
          ssid: jsonDecode["ssid"],
          psk: jsonDecode["pass"],
          timeout: 7500,
        })
        .then(() => {
          //* ファイル書込
          fs.writeFileSync(
            `${this.configDirPath}/Wifi.json`,
            `{ "ssid": "${jsonDecode["ssid"]}","pass": "${jsonDecode["pass"]}" }`
          );

          //* リターンログ
          returnLog["isConnect"] = true;
          console.log(JSON.stringify(returnLog));
        })
        .catch((error) => {
          //* リターンログ
          console.log(JSON.stringify(returnLog));
          console.error(error);
        });
    } // パース出来なかった場合
    else {
      //* リターンログ
      console.log(JSON.stringify(returnLog));
    }
  }

  connectFromFile() {
    try {
      this.connect(fs.readFileSync(`${this.configDirPath}/Wifi.json`, "utf-8"));
    } catch (error) {
      console.log('{ "isConnect": false }');
    }
  }
}

//* main
// wifiインスタンスを生成
wifi = new wifi();

//* getStatusを叩かれた場合
if (process.argv.length == 3 && process.argv[2] == "getStatus") {
  wifi.getStatus();
}

//* connectを叩かれた場合
if (process.argv.length == 4 && process.argv[2] == "connect") {
  wifi.connect(process.argv[3]);
}

//* connectFromFileを叩かれた場合
if (process.argv.length == 3 && process.argv[2] == "connectFromFile") {
  wifi.connectFromFile();
}
