from dotenv import load_dotenv
import json
import os
from pybleno import *
import subprocess
import sys
import signal
from Service_Register.Service_Register import Service_Register
from Service_Wifi.Service_Wifi import Service_Wifi


#* main.pyのパス
#print('abspath:     ', os.path.abspath(__file__))
#print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))
rootDirPath = os.path.dirname(os.path.abspath(__file__))

#* .envから環境変数を読み込み
load_dotenv(rootDirPath + "/../Config/.env")

#* ServiceUUID/UUIDをJSONから取り込む
json_open = open(rootDirPath + '/config/config.json', 'r')
json_load = json.load(json_open)
json_open.close()
#print(json_load)

#* Blenoインスタンスを生成
bleno = Bleno()

#* シリアルナンバーを取得するための関数
def getSerial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

#* シリアルナンバーを取得してデバイスネームを格納
raspPiSerialNumber = getSerial()
deviceName = "BerryLock_" + raspPiSerialNumber
os.environ["RASPPI_NUMBER"] = raspPiSerialNumber
os.environ["BLENO_DEVICE_NAME"] = deviceName

print("------------------------------")
print("Auto_Lock_BLE_Client")
print("SerialNumber: " + raspPiSerialNumber)
print("Initialize: " + deviceName)
print("Service_UUIDs: " + json_load['serviceUuids'])
print("API_URL: " + os.getenv("API_URL"))
print("------------------------------")


#* wifiの接続を試みる
try:
    res = subprocess.run(['/home/pi/.nodebrew/current/bin/node', rootDirPath + '/Service_Wifi/wifi.js','connectFromFile'],capture_output=True, check=True, text=True)
    isConnect = json.loads(res.stdout)
    print("  res.args: [" + str(res.args) + "]")
    print("  res.returncode: [" + str(res.returncode) + "]")
    print("  res.stdout: [" + str(res.stdout) + "]")
    print("  res.stderr: [" + str(res.stderr) + "]")
    print("  res.check_returncode: [" + str(res.check_returncode) + "]")
except Exception as error:
    isConnect["isConnect"] = False
    print("---------- Error ----------\n" + str(error))
finally:
    print(str(isConnect) + "\n")


def onStateChange(state):
    print("on -> stateChange: " + state)
    if (state == 'poweredOn'):
        bleno.startAdvertising(deviceName,[json_load['serviceUuids']])
    else:
        bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)


def onAdvertisingStart(error):
    print("on -> advertisingStart: " + ("error " + error if error else "success") + "\n")

    if not error:
        bleno.setServices([
            Service_Register(json_load['register']['uuidService'],json_load['register']['uuidGetOwner'],json_load['register']['uuidSetOwner'],json_load['register']['uuidUnsetOwner'],rootDirPath),
            Service_Wifi(json_load['wifi']['uuidService'],json_load['wifi']['uuidGetWifi'],json_load['wifi']['uuidSetWifi'],rootDirPath)
        ])

bleno.on("advertisingStart", onAdvertisingStart)


def onAccept(clientAddress):
    print("ble central connected: " + clientAddress)
    bleno.updateRssi()

bleno.on("accept", lambda clientAddress:onAccept(clientAddress))


bleno.on("disconnect", lambda clientAddress: print("ble central disconnected: " + str(clientAddress) + "\n"))
bleno.on("platform", lambda event: print("platform: " + str(event) + "\n"))
bleno.on("addressChange", lambda event: print("addressChange: " + str(event) + "\n"))
bleno.on("mtuChange", lambda event: print("mtuChange: " + str(event) + "\n"))
bleno.on("advertisingStartError", lambda event: print("advertisingStartError: " + str(event) + "\n"))
bleno.on("servicesSetError", lambda event: print("servicesSetError: " + str(event) + "\n"))
bleno.on("rssiUpdate", lambda event: print("rssiUpdate: " + str(event)));

bleno.start()

print ('Hit <ENTER> to disconnect')

if (sys.version_info > (3, 0)):
    input()
else:
    raw_input()

bleno.stopAdvertising()
bleno.disconnect()

print ('terminated.')
sys.exit(1)
