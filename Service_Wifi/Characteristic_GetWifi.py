import json
from pybleno import Characteristic
import array
import struct
import subprocess
import sys
import traceback

class Characteristic_GetWifi(Characteristic):
    #* コンストラクタ
    def __init__(self, uuid,rootDirPath):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read'],
            'value': None
        })
        self._rootDirPath = rootDirPath
        #print('abspath:     ', os.path.abspath(__file__))
        #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

    def onReadRequest(self, offset, callback):
        isConnect = None
        returnValue = None
        try:
            res = subprocess.run(['/home/pi/.nodebrew/current/bin/node', self._rootDirPath + '/Service_Wifi/wifi.js','getStatus'],capture_output=True,check=True, text=True)
            isConnect = json.loads(res.stdout)
            returnValue =  json.dumps(isConnect).encode(encoding='utf-8')
        except Exception as error:
            print(error)
            if(error.stdout != None):
                isConnect = json.loads(error.stdout)
            else:
                isConnect["isConnect"] = False
            returnValue = json.dumps(isConnect).encode(encoding='utf-8')

        print("Characteristic_GetWifi - %s - onReadRequest: value = %s" % (self["uuid"], isConnect))
        print("Characteristic_GetWifi - %s - onReadRequest: value = %s" % (self["uuid"], returnValue))
        print("\n")

        callback(Characteristic.RESULT_SUCCESS, returnValue)
