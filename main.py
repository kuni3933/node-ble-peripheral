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

#* ServiceUUID/UUIDをJSONから取り込む
json_open = open(rootDirPath + '/config/config.json', 'r')
json_load = json.load(json_open)
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
    return cpuserial.replace("00000000","")

#* シリアルナンバーを取得してデバイスネームを格納
raspPiSerialNumber = getSerial()
deviceName = "BerryLock_" + raspPiSerialNumber
os.environ["BLENO_DEVICE_NAME"] = deviceName

print("------------------------------")
print("bleno - echo")
print("SerialNumber: " + raspPiSerialNumber)
print("Initialize: " + deviceName)
print("------------------------------\n")

#* wifiの接続を試みる
res = subprocess.run(['/home/pi/.nodebrew/current/bin/node',rootDirPath + '/index.js','connectFromJson'],capture_output=True, text=True)
print("captured stdout: {}".format(res.stdout))

def onStateChange(state):
    print("on -> stateChange: " + state)
    if (state == 'poweredOn'):
        bleno.startAdvertising(deviceName)
    else:
        bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)


def onAdvertisingStart(error):
    print("on -> advertisingStart: " + ("error " + error if error else "success") + "\n")

    if not error:
        bleno.setServices([
            Service_Register(json_load['register']['uuidService'],json_load['register']['uuidGetOwner'],json_load['register']['uuidSetOwner'],json_load['register']['uuidUnsetOwner']),
            Service_Wifi(json_load['wifi']['uuidService'],json_load['wifi']['uuidGetWifi'],json_load['wifi']['uuidSetWifi'],rootDirPath)
        ])

bleno.on("advertisingStart", onAdvertisingStart)


def onAccept(clientAddress):
    print("ble central connected: " + clientAddress)
    bleno.updateRssi()

bleno.on("accept", lambda clientAddress:onAccept(clientAddress))


bleno.on("disconnect", lambda clientAddress: print("ble central disconnected: " + clientAddress + "\n"))
bleno.on("platform", lambda event: print("platform" + event))
bleno.on("addressChange", lambda event: print("addressChange", event))
bleno.on("mtuChange", lambda event: print("mtuChange", event))
bleno.on("advertisingStartError", lambda event: print("advertisingStartError", event))
bleno.on("servicesSetError", lambda event: print("servicesSetError", event))
#bleno.on("rssiUpdate", lambda event: print("rssiUpdate" + event));

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
