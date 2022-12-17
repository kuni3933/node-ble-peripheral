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
        print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [data.decode(encoding='utf-8')]))
        print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in data]))

        isConnect = None
        try:
            res = subprocess.run(['/home/pi/.nodebrew/current/bin/node', self._rootDirPath + '/Service_Wifi/wifi.js','connect','\'' + data.decode(encoding='utf-8') + '\''],capture_output=True, text=True)
            isConnect = json.loads(res.stdout)
        except Exception as error:
            print(error)
            if(error.stdout != None):
                isConnect = json.loads(error.stdout)
            else:
                isConnect["isConnect"] = False
        finally:
            print(isConnect)
            print('\n')

        if((isConnect != None) & (isConnect["isConnect"] == True)):
            callback(Characteristic.RESULT_SUCCESS)
        else:
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
