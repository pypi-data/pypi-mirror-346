# ********************************************************************
#
#  $Id: helloworld.py 66295 2025-05-06 10:27:20Z seb $
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
from yoctolib.yocto_currentloopoutput import YCurrentLoopOutput
from yoctolib.yocto_voltageoutput import YVoltageOutput


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
    # retrieve any VoltageOutput function
    loop: YCurrentLoopOutput = YCurrentLoopOutput.FirstCurrentLoopOutput()
    if loop is None:
        die('No module connected')
    target = loop.get_serialNumber()

# retrieve both channels
loop: YCurrentLoopOutput = YCurrentLoopOutput.FindCurrentLoopOutput(target + '.currentLoopOutput')

if not loop.isOnline():
    die('device not connected')

values = [4.0, 10.0, 19.0, 4.0]
for v in values:
    print("Change output to %f" % v)
    # output 1: immediate change
    loop.set_current(v)
    loopPower = loop.get_loopPower()
    if loopPower == YCurrentLoopOutput.LOOPPOWER_NOPWR:
        print("Current loop not powered")
    elif loopPower == YCurrentLoopOutput.LOOPPOWER_NOPWR:
        print("Insufficient voltage on current loop")
    else:
        print("current loop set to " + str(v) + " mA")
    YAPI.Sleep(1000)
YAPI.FreeAPI()
