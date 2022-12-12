from pybleno import BlenoPrimaryService
from .Characteristic_GetWifi import Characteristic_GetWifi
from .Characteristic_SetWifi import Characteristic_SetWifi

class Service_Wifi(BlenoPrimaryService):
    #* コンストラクタ
    def __init__(self, uuidService,uuidGetWifi,uuidSetWifi):
        BlenoPrimaryService.__init__(self,{
            'uuid': uuidService,
            'characteristics': [
                Characteristic_GetWifi(uuidGetWifi),
                Characteristic_SetWifi(uuidSetWifi)
            ]
        })

