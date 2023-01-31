import json
import os
from pybleno import Characteristic
import array
import struct
import subprocess
import sys
import traceback

class Characteristic_Wifi(Characteristic):
    #* コンストラクタ
    def __init__(self, uuid,rootDirPath):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read','write'],
            'value': None
        })
        self._rootDirPath = rootDirPath
        #print('abspath:     ', os.path.abspath(__file__))
        #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))


    def onReadRequest(self, offset, callback):
        err = None
        isConnect = {"isConnect":False}
        res = None
        returnValue = None

        try:
            res = subprocess.run(['/home/pi/.nodebrew/current/bin/node', self._rootDirPath + '/Service_Wifi/wifi.js','getStatus'],capture_output=True,check=True, text=True)
            isConnect = json.loads(res.stdout)
            returnValue =  json.dumps(isConnect).encode(encoding='utf-8')
        except Exception as error:
            isConnect["isConnect"] = False
            returnValue = json.dumps(isConnect).encode(encoding='utf-8')
            err = error
        finally:
            print("Characteristic_Wifi - %s - onReadRequest: value = %s" % (self["uuid"], isConnect))
            print("Characteristic_Wifi - %s - onReadRequest: value = %s" % (self["uuid"], returnValue))
            if(res != None):
                print("  res.args: [" + str(res.args) + "]" )
                print("  res.returncode: [" + str(res.returncode) + "]" )
                print("  res.stdout: [" + str(res.stdout) + "]")
                print("  res.stderr: [" + str(res.stderr) + "]")
                print("  res.check_returncode: [" + str(res.check_returncode) + "]")
            if(err != None):
                print("---------- Error ----------\n" + str(err))
            print("\n")
        callback(Characteristic.RESULT_SUCCESS, returnValue)


    def onWriteRequest(self, data, offset, withoutResponse, callback):
        dataDecoded = None
        dataDecodedErr = None
        isConnect = {"isConnect":False}

        try:
            dataDecoded = data.decode(encoding='utf-8')
        except Exception as error:
            print('Characteristic_Wifi - %s - onWriteRequest: value = %s' % (self['uuid'], ["Error: Could not decode data to UTF-8."]))
            dataDecoded = None
            dataDecodedErr = error
        else:
            print('Characteristic_Wifi - %s - onWriteRequest: value = %s' % (self['uuid'], [dataDecoded]))
        finally:
            print('Characteristic_Wifi - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in data]))
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

        callback(Characteristic.RESULT_SUCCESS)
