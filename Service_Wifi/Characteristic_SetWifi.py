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
        dataDecoded = None
        dataDecodedErr = None
        isConnect = {"isConnect":False}

        try:
            dataDecoded = data.decode(encoding='utf-8')
        except Exception as error:
            print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], ["Error: Could not decode data to UTF-8."]))
            dataDecoded = None
            dataDecodedErr = error
        else:
            print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [dataDecoded]))
        finally:
            print('Characteristic_SetWifi - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in data]))
            if(dataDecodedErr != None):
                print("---------- Error ----------\n" + str(dataDecodedErr))
                dataDecodedErr = None

        if(dataDecoded != None):
            try:
                res = subprocess.run(['/home/pi/.nodebrew/current/bin/node', self._rootDirPath + '/Service_Wifi/wifi.js','connect', dataDecoded], capture_output=True, check=True, text=True)
                isConnect = json.loads(res.stdout)
                print("  res.args: [" + str(res.args) + "]" )
                print("  res.returncode: [" + str(res.returncode) + "]" )
                print("  res.stdout: [" + str(res.stdout) + "]")
                print("  res.stderr: [" + str(res.stderr) + "]")
                print("  res.check_returncode: [" + str(res.check_returncode) + "]")
            except Exception as error:
                print("---------- Error ----------\n" + str(error))
                isConnect["isConnect"] = False
            finally:
                print(str(isConnect) + "\n\n")
                if(isConnect["isConnect"] == True):
                    callback(Characteristic.RESULT_SUCCESS)
                else:
                    callback(Characteristic.RESULT_UNLIKELY_ERROR)
        else:
            print(str(isConnect) + "\n\n")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
