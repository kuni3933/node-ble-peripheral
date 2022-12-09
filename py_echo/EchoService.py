from pybleno import BlenoPrimaryService
from EchoCharacteristic import *

class EchoService(BlenoPrimaryService):
    #* コンストラクタ
    def __init__(self, uuid):
        BlenoPrimaryService.__init__(self,{
            'uuid': uuid,
            'characteristics': [
                EchoCharacteristic('ec0F')
            ]
        })

