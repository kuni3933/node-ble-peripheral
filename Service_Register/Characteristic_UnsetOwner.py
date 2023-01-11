from pybleno import Characteristic
import array
import json
import os
import requests
import struct
import sys
import traceback

class Characteristic_UnsetOwner(Characteristic):
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
        isSuccess = False

        try:
            dataDecoded = data.decode(encoding='utf-8')
            print('Characteristic_UnsetOwner - %s - onWriteRequest: value = \n%s' % (self['uuid'], [dataDecoded]))
        except Exception as error:
            print('Characteristic_UnsetOwner - %s - onWriteRequest: value = %s' % (self['uuid'], ["Error: Could not decode data to UTF-8."]))
            print('Characteristic_UnsetOwner - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in data]))
            print("---------- Error ----------\n" + str(error))
            dataDecoded = None

        if(dataDecoded != None):
            try:
                data = {
                    'Token' : json.loads(dataDecoded)["idToken"],
                    'x509' : os.getenv("RASPPI_NUMBER"),
                }
                #print(data)
                res = requests.delete(os.getenv("API_URL") + "/v1/rasppi",data=data)
                print("  res.status_code: [" + str(res.status_code) + "]")
                print("  res.response.headers:")
                for key,value in res.headers.items():
                    print("    " + key,'   ',value)
                print("  res.encoding: [" + str(res.encoding) + "]")
                print("  res.text: [" + str(res.text) + "]")

                if(res.status_code == 204):
                    isSuccess = True
                    os.remove(self._rootDirPath + "/../Config/customToken.json")
                    os.remove(self._rootDirPath + "/../Config/ownerUid.json")

            except Exception as error:
                print("---------- Error ----------\n" + str(error))
                isSuccess = False
            finally:
                print("isSuccess: " + str(isSuccess) + "\n\n")
                if(isSuccess == True):
                    callback(Characteristic.RESULT_SUCCESS)
                else:
                    callback(Characteristic.RESULT_UNLIKELY_ERROR)
        else:
            print("isSuccess: " + str(isSuccess) + "\n\n")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
