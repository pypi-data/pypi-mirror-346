# ********************************************************************
#
#  $Id: helloworld.py 66294 2025-05-06 10:17:53Z seb $
#
#  An example that show how to use a  Yocto-Meteo
#
#  You can find more information on our web site:
#   Yocto-Meteo documentation:
#      https://www.yoctopuce.com/EN/products/yocto-meteo/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************
import sys

from yoctolib.yocto_api import YRefParam, YAPI
from yoctolib.yocto_genericsensor import YGenericSensor


def die(msg):
    YAPI.FreeAPI()
    sys.exit(msg + ' (check USB cable)')


# the API use local USB devices through VirtualHub
errmsg: YRefParam = YRefParam()
if YAPI.RegisterHub("localhost", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub failed: " + errmsg.value)

# To use a specific device, invoke the script as
#   python helloworld.py [serial_number]
# or
#   python helloworld.py [logical_name]
target: str = 'any'
if len(sys.argv) > 1:
    target = sys.argv[1]

if target == 'any':
    # retrieve any humidity sensor
    sensor: YGenericSensor = YGenericSensor.FirstGenericSensor()
    if sensor is None:
        die('No module connected')
    target = sensor.get_serialNumber()

# retrieve both channels
channel1: YGenericSensor = YGenericSensor.FindGenericSensor(target + '.genericSensor1')
channel2: YGenericSensor = YGenericSensor.FindGenericSensor(target + '.genericSensor2')
if not channel1.isOnline():
    die("Yocto-0-10-V-Rx '%s' not connected" % target)

print("Use device %s" % channel1.get_serialNumber())
while channel1.isOnline():
    print("channel 1:  %f %s" % (channel1.get_currentValue(), channel1.get_unit()))
    print("channel 2:  %f %s" % (channel2.get_currentValue(), channel2.get_unit()))
    print("  (Ctrl-C to stop)")
    YAPI.Sleep(1000)

YAPI.FreeAPI()
