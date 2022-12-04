from pybleno import Characteristic
import array
import struct
import sys
import traceback

class EchoCharacteristic(Characteristic):
    #* コンストラクタ
    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
        })
        self._value = None
        self._updateValueCallback = None

    def onReadRequest(self, callback):
        print('EchoCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], self._value))
        callback(Characteristic.RESULT_SUCCESS, self._value)

    def onWriteRequest(self, data, callback):
        self._value = data
        print('EchoCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], self._value))
        if self._updateValueCallback:
            print('EchoCharacteristic - onWriteRequest: notifying');
            self._updateValueCallback(self._value)
        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, updateValueCallback):
        print('EchoCharacteristic - onSubscribe')
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('EchoCharacteristic - onUnsubscribe');
        self._updateValueCallback = None
