import time
import datetime
import smbus
from bh1750 import BH1750



bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
_lightSensor = BH1750(bus)
_illuminance = 0.0
_illuminanceSaved = 0.0

_checkTime = True
_offCounter = 0


_startDateTime = datetime.datetime.now()


while (_checkTime):

    _lightSensor.set_sensitivity(255)
    _illuminance = _lightSensor.measure_low_res()

    #Only store the data if the difference is more than one lux 
    if (abs(_illuminanceSaved - _illuminance) >= 1):

        #Save the current light intensity value
        _illuminanceSaved = _illuminance

        #Calculate the time since start hh:mm:ss
        _differenceDateTime = datetime.datetime.now() - _startDateTime
        _strDifferenceDateTime = str(int(_differenceDateTime.seconds / 3600)) + ":" + (str(int(_differenceDateTime.seconds / 60)) + ":" + str(_differenceDateTime.seconds))

        _file = open("LightCheck.txt", "a")  
        _file.write((_strDifferenceDateTime + "\t{:.2f}".format(_illuminance) + "\n").replace(".", ","))

        print((_strDifferenceDateTime + " Light: {:.2f} lux".format(_illuminance)).replace(".", ","))
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
