import json
import os
from pybleno import Characteristic
import array
import struct
import subprocess
import sys
import traceback

class Characteristic_SetWifi(Characteristic):
    #* コンストラクタ
    def __init__(self, uuid,rootDirPath):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['write'],
            'value': None
        })
        self._rootDirPath = rootDirPath
        #print('abspath:     ', os.path.abspath(__file__))
        #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        dataDecoded = data.decode(encoding='utf-8')
        isConnect = None
        err = None

        print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [dataDecoded]))
        print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in data]))

        try:
            res = subprocess.run(['/home/pi/.nodebrew/current/bin/node', self._rootDirPath + '/Service_Wifi/wifi.js','connect'],capture_output=True, check=True, input=dataDecoded,text=True)
            isConnect = json.loads(res.stdout)
            if(res.stderr):
                err += "---------- Stderr ----------\n" + res.stderr
        except Exception as error:
            isConnect["isConnect"] = False
            err += "---------- Error ----------\n" +  error
        finally:
            if((isConnect != None) & (isConnect["isConnect"] == True)):
                callback(Characteristic.RESULT_SUCCESS)
            else:
                callback(Characteristic.RESULT_UNLIKELY_ERROR)
            print(isConnect)
            print(err + "\n")

