import os
from pybleno import Characteristic
import array
import struct
import sys
import traceback

class Characteristic_SetWifi(Characteristic):
    #* コンストラクタ
    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write'],
            'value': None
        })
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
        print('abspath:     ', os.path.abspath(__file__))
        print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

    def onReadRequest(self, offset, callback):
        print('Characteristic_SetWifi - %s - onReadRequest: value = %s' % (self['uuid'], [self._value.decode()]))
        print('Characteristic_SetWifi - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('\n')
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [self._value.decode()]))
        print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('\n')
        callback(Characteristic.RESULT_SUCCESS)
