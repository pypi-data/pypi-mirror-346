# ********************************************************************
#
#  $Id: helloworld.py 66289 2025-05-06 09:19:35Z seb $
#
#  An example that show how to use a  Yocto-Knob
#
#  You can find more information on our web site:
#   Yocto-Knob documentation:
#      https://www.yoctopuce.com/EN/products/yocto-knob/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************
import sys

from yoctolib.yocto_api import YAPI, YRefParam
from yoctolib.yocto_current import YCurrent
from yoctolib.yocto_voltage import YVoltage


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
    # retrieve any compatible module
    func: YCurrent = YCurrent.FirstCurrent()
    if func is None:
        die('No Yocto-Amp connected')
    target = func.get_serialNumber()

# we need to retrieve both DC and AC voltage from the device.
sensorDC: YCurrent = YCurrent.FindCurrent(target + '.current1')
sensorAC: YCurrent = YCurrent.FindCurrent(target + '.current2')

if not sensorAC.isOnline():
    die('Module not connected')

while sensorAC.isOnline():
    print('DC: ' + str(sensorDC.get_currentValue()) + ' mA ' + \
          'AC: ' + str(sensorAC.get_currentValue()) + ' mA ')
    print('  (press Ctrl-C to exit)')
    YAPI.Sleep(1000, errmsg)
YAPI.FreeAPI()
