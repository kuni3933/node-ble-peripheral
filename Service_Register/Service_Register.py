from pybleno import BlenoPrimaryService
from .Characteristic_GetOwner import Characteristic_GetOwner
from .Characteristic_SetOwner import Characteristic_SetOwner
from .Characteristic_UnsetOwner import Characteristic_UnsetOwner

class Service_Register(BlenoPrimaryService):
    #* コンストラクタ
    def __init__(self, uuidService,uuidGetOwner,uuidSetOwner,uuidUnsetOwner,rootDirPath):
        BlenoPrimaryService.__init__(self,{
            'uuid': uuidService,
            'characteristics': [
                Characteristic_GetOwner(uuidGetOwner,rootDirPath),
                Characteristic_SetOwner(uuidSetOwner,rootDirPath),
                Characteristic_UnsetOwner(uuidUnsetOwner,rootDirPath)
            ]
        })

