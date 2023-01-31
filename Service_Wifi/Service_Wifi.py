from pybleno import BlenoPrimaryService
from .Characteristic_Wifi import Characteristic_Wifi

class Service_Wifi(BlenoPrimaryService):
    #* コンストラクタ
    def __init__(self, uuidService,uuidWifi,rootDirPath):
        BlenoPrimaryService.__init__(self,{
            'uuid': uuidService,
            'characteristics': [
                Characteristic_Wifi(uuidWifi,rootDirPath)
            ]
        })
