import { fileURLToPath } from "url";
import fs from "fs";
import path from "path";
import rpi_wifi_connection from "rpi-wifi-connection";

class wifi {
  //* プロパティ
  _configDirPath;
  _wifi;

  //* コンストラクタ
  constructor() {
    //* wifiインスタンスを生成
    this._wifi = new rpi_wifi_connection();

    //* Configディレクトリのパス
    this._configDirPath = `${path.dirname(
      fileURLToPath(import.meta.url)
    )}/../../Config`;
    //process.stdout.write(`_configDirPath: ${this._configDirPath}`);
  }

  //* メソッド
  async getStatus() {
    await this._wifi
      .getStatus()
      .then((status) => {
        if (status.ssid != undefined) {
          status["isConnect"] = true;
        } else {
          status["isConnect"] = false;
        }
        process.stdout.write(JSON.stringify(status));
      })
      .catch((error) => {
        process.stdout.write(JSON.stringify({ isConnect: false }));
        console.error(error);
      });
  }

  async connect(json) {
    // リターンログ用オブジェクト(初期値:false)
    let returnLog = { isConnect: false };

    try {
      // コマンドライン引数からjsonをパース
      const jsonDecoded = JSON.parse(json);

      // 正常にjsonをパース && ssid/passが存在 の場合はconnect
      if (
        jsonDecoded["ssid"] != undefined &&
        jsonDecoded["pass"] != undefined
      ) {
        await this._wifi
          .connect({
            ssid: jsonDecoded["ssid"],
            psk: jsonDecoded["pass"],
            timeout: 15000,
          })
          .then(() => {
            //* ファイル書込
            fs.writeFileSync(
              `${this._configDirPath}/Wifi.json`,
              `{ "ssid": "${jsonDecoded["ssid"]}","pass": "${jsonDecoded["pass"]}" }`
            );

            //* リターンログをtrue
            returnLog["isConnect"] = true;
          })
          .catch((error) => {
            throw error;
          });
      }
    } catch (error) {
      // 再度isConnectをfalse
      returnLog["isConnect"] = false;
      console.error(error);
    } finally {
      process.stdout.write(JSON.stringify(returnLog));
    }
  }

  async connectFromFile() {
    try {
      await this.connect(
        fs.readFileSync(`${this._configDirPath}/Wifi.json`, "utf-8")
      );
    } catch (error) {
      process.stdout.write(JSON.stringify({ isConnect: false }));
      console.error(error);
    }
  }
}

//* main
// wifiインスタンスを生成
wifi = new wifi();
switch (true) {
  case process.argv[2] === "getStatus":
    //* getStatusを叩かれた場合
    await wifi.getStatus();
    break;

  case process.argv[2] === "connect" && process.argv[3] != undefined:
    //* connectを叩かれた場合
    await wifi.connect(process.argv[3]);
    break;

  case process.argv[2] === "connectFromFile":
    //* connectFromFileを叩かれた場合
    await wifi.connectFromFile();
    break;

  default:
    //* 対処外のコマンド引数を叩かれた場合
    process.stdout.write(
      JSON.stringify({ error: "CommandNotFound", isConnect: false })
    );
}
