import os
from pybleno import *
import sys
import signal
from EchoCharacteristic import *

print('bleno - echo');
bleno = Bleno()


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial.replace("00000000","")

raspPiSerialNumber = getserial()
deviceName = "BerryLock_" + raspPiSerialNumber
os.environ["BLENO_DEVICE_NAME"] = deviceName
print("------------------------------")
print("SerialNumber: " + raspPiSerialNumber)
print("Initialize: " + deviceName)
print("------------------------------\n")


def onStateChange(state):
    print('on -> stateChange: ' + state);
    if (state == 'poweredOn'):
        bleno.startAdvertising('echo', ['ec00'])
    else:
        bleno.stopAdvertising();

bleno.on('stateChange', onStateChange)

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'));

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': 'ec00',
                'characteristics': [
                    EchoCharacteristic('ec0F')
                    ]
            })
        ])

bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()

print ('Hit <ENTER> to disconnect')

if (sys.version_info > (3, 0)):
    input()
else:
    raw_input()

bleno.stopAdvertising()
bleno.disconnect()

print ('terminated.')
sys.exit(1)
