from pybleno import Characteristic
import array
import struct
import sys
import traceback

class Characteristic_UnsetOwner(Characteristic):
    #* コンストラクタ
    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['write'],
            'value': None
        })
        self._value = "null".encode(encoding='utf-8')
        self._updateValueCallback = None
        #print('abspath:     ', os.path.abspath(__file__))
        #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

    def onReadRequest(self, offset, callback):
        print('Characteristic_UnsetOwner - %s - onReadRequest: value = %s' % (self['uuid'], [self._value.decode(encoding='utf-8')]))
        print('Characteristic_UnsetOwner - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('\n')
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('Characteristic_UnsetOwner - %s - onWriteRequest: value = %s' % (self['uuid'], [self._value.decode(encoding='utf-8')]))
        print('Characteristic_UnsetOwner - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('\n')
        callback(Characteristic.RESULT_SUCCESS)
