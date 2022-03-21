import time
import smbus
from bh1750 import BH1750



bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
_lightSensor = BH1750(bus)
_illuminance = 0.0


_checkTime = True
_offCounter = 0

while (_checkTime):

    _lightSensor.set_sensitivity(255)
    _illuminance = _lightSensor.measure_low_res()


    _currentTime = time.strftime("%H:%M:%S", time.localtime())

    _file = open("LightCheck.txt", "a")  
    _file.write(_currentTime + " Light: {:.2f} lux".format(_illuminance) + "\n")

    print("Light: {:.2f} lux".format(_illuminance))
    time.sleep(120)

    _file.close()

    if (_illuminance == 0):
        _offCounter = _offCounter +1


    if (_offCounter > 3):
        _checkTime = False
