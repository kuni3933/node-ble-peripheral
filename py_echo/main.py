import os
from pybleno import *
import sys
import signal
from EchoService import *

bleno = Bleno()

def getSerial():
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
raspPiSerialNumber = getSerial()
deviceName = "BerryLock_" + raspPiSerialNumber
os.environ["BLENO_DEVICE_NAME"] = deviceName

print("bleno - echo")
print("------------------------------")
print("SerialNumber: " + raspPiSerialNumber)
print("Initialize: " + deviceName)
print("------------------------------\n")


def onStateChange(state):
    print("on -> stateChange: " + state)
    if (state == 'poweredOn'):
        bleno.startAdvertising('echo', ['ec00'])
    else:
        bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)


def onAdvertisingStart(error):
    print("on -> advertisingStart: " + ("error " + error if error else "success") + "\n")

    if not error:
        bleno.setServices([
            EchoService('ec00')
        ])

bleno.on("advertisingStart", onAdvertisingStart)


def onAccept(clientAddress):
    print("ble central connected: " + clientAddress)
    bleno.updateRssi()

bleno.on("accept", lambda clientAddress:onAccept(clientAddress))


bleno.on("disconnect", lambda clientAddress: print("ble central disconnected: " + clientAddress + "\n"))
bleno.on("platform", lambda event: print("platform" + event))
bleno.on("addressChange", lambda event: print("addressChange", event))
bleno.on("mtuChange", lambda event: print("mtuChange", event))
bleno.on("advertisingStartError", lambda event: print("advertisingStartError", event))
bleno.on("servicesSetError", lambda event: print("servicesSetError", event))
#bleno.on("rssiUpdate", lambda event: print("rssiUpdate" + event));

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
