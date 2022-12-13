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
        self._value = "null".encode(encoding='utf-8')
        self._updateValueCallback = None
        #print('abspath:     ', os.path.abspath(__file__))
        #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

    def onReadRequest(self, offset, callback):
        print('Characteristic_SetWifi - %s - onReadRequest: value = %s' % (self['uuid'], [self._value.decode(encoding='utf-8')]))
        print('Characteristic_SetWifi - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('\n')
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [self._value.decode(encoding='utf-8')]))
        print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))

        jsonLoad = None
        try:
            jsonLoad = json.loads(data.decode(encoding='utf-8'))
        except Exception as e:
            jsonLoad = None
            print('---------- Error ----------')
            print(str(e) + '\n')

        if(jsonLoad):
            res = subprocess.run(['/home/pi/.nodebrew/current/bin/node', self._rootDirPath + '/index.js','connect',jsonLoad['ssid'],jsonLoad['pass']],capture_output=True, text=True)
            isConnect = json.loads(res.stdout)
            print(isConnect)
            print('\n')

            if(isConnect['isConnect']):
                callback(Characteristic.RESULT_SUCCESS)
            else:
                callback(Characteristic.RESULT_UNLIKELY_ERROR)
        else:
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
