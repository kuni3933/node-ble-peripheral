import array
import json
import os
import struct
import sys
import traceback

def onRead(name,uuid,rootDirPath):
    # パスを組み立てる
    ownerUidJsonPath = rootDirPath + "/../Config/ownerUid.json"

    # Ownerのuidを初期値としてnullに設定
    ownerUid = {"uid": "Null"}

    # ファイル読込時のエラー
    jsonReadError = None

    # ownerUid.jsonがあるか確認
    isFileExists = os.path.isfile(ownerUidJsonPath)
    #print(isFileExists)

    # ファイルが存在した場合
    if (isFileExists == True):
        try:
            # 読み込んでuidを取得
            json_open = open(ownerUidJsonPath,"r")
            ownerUid["uid"] = json.load(json_open)["ownerUid"]
            json_open.close()
            #print(json_load)
            #print("customToken: " + json_load['customToken'] + "\nuid: " + json_load["uid"])
        except Exception as error:
            jsonReadError = error
            ownerUid["uid"] = "Null"

    returnValue = json.dumps(ownerUid).encode(encoding='utf-8')
    print('Characteristic_%sOwner - %s - onReadRequest: value = %s' % (name,uuid, ownerUid))
    print('Characteristic_%sOwner - %s - onReadRequest: value = %s' % (name,uuid, returnValue))

    if(jsonReadError != None):
        print("---------- Error ----------\n" + str(jsonReadError))
        jsonReadError = None
    print('\n')

    return returnValue
