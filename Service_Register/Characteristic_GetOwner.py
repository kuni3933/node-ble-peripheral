from pybleno import Characteristic
import array
import json
import os
import struct
import sys
import traceback

class Characteristic_GetOwner(Characteristic):
    #* コンストラクタ
    def __init__(self, uuid,rootDirPath):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read',],
            'value': None
        })
        self._rootDirPath = rootDirPath
        #print('abspath:     ', os.path.abspath(__file__))
        #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

    def onReadRequest(self, offset, callback):
        # Ownerのuidを初期値としてnullに設定
        ownerUid = {"uid": "Null"}

        # ファイル読込時のエラー
        jsonReadError = None

        # ownerUid.jsonがあるか確認
        isFileExists = os.path.isfile(self._rootDirPath + "/../Config/ownerUid.json")
        #print(isFileExists)

        # ファイルが存在した場合
        if (isFileExists == True):
            try:
                # 読み込んでuidを取得
                json_open = open(self._rootDirPath + "/../Config/ownerUid.json","r")
                ownerUid["uid"] = json.load(json_open)["ownerUid"]
                json_open.close()
                #print(json_load)
                #print("customToken: " + json_load['customToken'] + "\nuid: " + json_load["uid"])
            except Exception as error:
                jsonReadError = error
                ownerUid["uid"] = "Null"

        returnValue = json.dumps(ownerUid).encode(encoding='utf-8')
        print('Characteristic_GetOwner - %s - onReadRequest: value = %s' % (self['uuid'], ownerUid))
        print('Characteristic_GetOwner - %s - onReadRequest: value = %s' % (self['uuid'], returnValue))
        if(jsonReadError != None):
            print("---------- Error ----------\n" + str(jsonReadError))
            jsonReadError = None
        print('\n')
        callback(Characteristic.RESULT_SUCCESS, returnValue)
