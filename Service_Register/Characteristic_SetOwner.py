from pybleno import Characteristic
import array
import json
import os
import requests
import struct
import sys
import traceback

class Characteristic_SetOwner(Characteristic):
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
        isSuccess = False
        dataDecoded = None
        resCustomToken = None
        resRefreshToken = None
        resUnsetOwner = None

        try:
            dataDecoded = data.decode(encoding='utf-8')
            print('Characteristic_SetOwner - %s - onWriteRequest: value = \n%s' % (self['uuid'], [dataDecoded]))
        except Exception as error:
            print('Characteristic_SetOwner - %s - onWriteRequest: value = %s' % (self['uuid'], ["Error: Could not decode data to UTF-8."]))
            print('Characteristic_SetOwner - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in data]))
            print("---------- Error ----------\n" + str(error))
            dataDecoded = None

        #* 正常にデコード出来ていたらAPIへトークンPOSTしてcustomTokenを取得
        if(dataDecoded != None):
            try:
                #* カスタムトークンの生成
                dataCustomToken = {
                    'Token' : json.loads(dataDecoded)["idToken"],
                    'x509' : os.getenv("RASPPI_NUMBER"),
                }
                #print(dataCustomToken)
                print("--resCustomToken:")
                resCustomToken = requests.post(os.getenv("API_URL") + "/v1/rasppi",data = dataCustomToken)
                print("  resCustomToken.status_code: [" + str(resCustomToken.status_code) + "]")
                print("  resCustomToken.headers:")
                for key,value in resCustomToken.headers.items():
                    print("    " + key,'   ',value)
                print("  resCustomToken.encoding: [" + str(resCustomToken.encoding) + "]")
                print("  resCustomToken.text: [" + str(resCustomToken.text) + "]")
            except Exception as error:
                print("---------- error ----------\n" + str(error))
        #* カスタムトークンを取得できていた場合は、取得トークンを使用してリフレッシュトークンの生成
        if(resCustomToken != None and resCustomToken.status_code == 201):
            try:
                headers = {
                    'Content-Type': 'application/json',
                }
                dataRefreshToken = {
                    'token' : json.loads(resCustomToken.text)["customToken"],
                    'returnSecureToken' : True,
                }
                #print(dataRefreshToken)
                resRefreshToken = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=" + os.getenv("FIREBASE_apiKey"),headers=headers, data=json.dumps(dataRefreshToken).encode('utf-8'))
                print("--resRefreshToken:")
                print("  resRefreshToken.status_code: [" + str(resRefreshToken.status_code) + "]")
                print("  resRefreshToken.headers:")
                for key,value in resRefreshToken.headers.items():
                    print("    " + key,'   ',value)
                print("  resRefreshToken.encoding: [" + str(resRefreshToken.encoding) + "]")
                print("  resRefreshToken.text: [" + str(resRefreshToken.text) + "]")
                isSuccess = True
            except Exception as error:
                print("---------- error ----------\n" + str(error))

        #* customToken/refreshToken の両方が取得できた場合はファイル書き込み
        if(resCustomToken != None and resCustomToken.status_code == 201 and resRefreshToken != None and resRefreshToken.status_code == 200):
            try:
                # ownerUid.json
                file = open(self._rootDirPath + "/../Config/ownerUid.json","w")
                file.write(json.dumps({"ownerUid": json.loads(resCustomToken.text)["ownerUid"]},indent=2) + "\n")
                file.close()
                # customToken.json
                file = open(self._rootDirPath + "/../Config/customToken.json","w")
                file.write(resRefreshToken.text)
                file.close()
            except Exception as error:
                isSuccess = False
                if(os.path.isfile(self._rootDirPath + "/../Config/ownerUid.json")):
                    os.remove(self._rootDirPath + "/../Config/ownerUid.json")
                if(os.path.isfile(self._rootDirPath + "/../Config/customToken.json")):
                    os.remove(self._rootDirPath + "/../Config/customToken.json")

        #* カスタムトークンしか取得できなかった/ファイル書き込みに失敗した場合はUnsetのために再度APIへPOST
        if(isSuccess == False and resCustomToken != None and resCustomToken.status_code == 201):
            try:
                dataUnsetOwner = {
                    'Token' : json.loads(dataDecoded)["idToken"],
                    'x509' : os.getenv("RASPPI_NUMBER"),
                }
                #print(dataUnsetOwner)
                print("--resUnsetOwner:")
                resUnsetOwner = requests.delete(os.getenv("API_URL") + "/v1/rasppi",data = dataUnsetOwner)
                print("  resUnsetOwner.status_code: [" + str(resUnsetOwner.status_code) + "]")
                print("  resUnsetOwner.headers:")
                for key,value in resUnsetOwner.headers.items():
                    print("    " + key,'   ',value)
                print("  resUnsetOwner.encoding: [" + str(resUnsetOwner.encoding) + "]")
                print("  resUnsetOwner.text: [" + str(resUnsetOwner.text) + "]")
            except Exception as error:
                print("---------- error ----------\n" + str(error))

        print("isSuccess: " + str(isSuccess) + "\n\n")
        if(isSuccess == True):
            callback(Characteristic.RESULT_SUCCESS)
        else:
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
