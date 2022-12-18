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
            print("Characteristic_GetWifi - %s - onReadRequest: value = %s" % (self["uuid"], isConnect))
            print("Characteristic_GetWifi - %s - onReadRequest: value = %s" % (self["uuid"], returnValue))
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
