from pybleno import Characteristic
import array
import struct
import sys
import traceback

class Characteristic_SetOwner(Characteristic):
    #* コンストラクタ
    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write'],
            'value': None
        })
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        print('Characteristic_SetOwner - %s - onReadRequest: value = %s' % (self['uuid'], [self._value.decode()]))
        print('Characteristic_SetOwner - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('\n')
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('Characteristic_SetOwner - %s - onWriteRequest: value = %s' % (self['uuid'], [self._value.decode()]))
        print('Characteristic_SetOwner - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('\n')
        callback(Characteristic.RESULT_SUCCESS)
