import time
import smbus
from bh1750 import BH1750



bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
_lightSensor = BH1750(bus)
_illuminance = 0.0
_illuminanceSaved = 0.0

_checkTime = True
_offCounter = 0

while (_checkTime):

    _lightSensor.set_sensitivity(255)
    _illuminance = _lightSensor.measure_low_res()

    #Only store the data if the difference is more than one lux 
    if (abs(_illuminanceSaved - _illuminance) >= 1):

        #Save the current value
        _illuminanceSaved = _illuminance

        _currentTime = time.strftime("%H:%M:%S", time.localtime())

        _file = open("LightCheck.csv", "a")  
        _file.write(_currentTime + ";{:.2f}".format(_illuminance) + "\n")

        print("Light: {:.2f} lux".format(_illuminance))
        _file.close()

    
    time.sleep(120)


    #Check if the light is off 
    if (_illuminance == 0):
        _offCounter = _offCounter +1
    else:
        _offCounter = 0

    #If the light is off three times in a row we stop the application
    if (_offCounter > 3):
        _checkTime = False
