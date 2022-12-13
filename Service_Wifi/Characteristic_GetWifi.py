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
        self._value = "null".encode(encoding='utf-8')
        self._updateValueCallback = None
        #print('abspath:     ', os.path.abspath(__file__))
        #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

    def onReadRequest(self, offset, callback):
        res = subprocess.run(['/home/pi/.nodebrew/current/bin/node', self._rootDirPath + '/index.js','getStatus'],capture_output=True, text=True)
        isConnect = json.loads(res.stdout)
        returnValue = json.dumps(isConnect).encode(encoding='utf-8')

        print('Characteristic_GetWifi - %s - onReadRequest: value = %s' % (self['uuid'], isConnect))
        print('Characteristic_GetWifi - %s - onReadRequest: value = %s' % (self['uuid'], returnValue))
        print('\n')

        callback(Characteristic.RESULT_SUCCESS, returnValue)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('Characteristic_GetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [self._value.decode(encoding='utf-8')]))
        print('Characteristic_GetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('\n')
        callback(Characteristic.RESULT_SUCCESS)
