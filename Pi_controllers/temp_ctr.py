from subprocess import Popen, PIPE
import RPi.GPIO as GPIO 
from collections import deque
import syslog


class fan_control():
    
    def __init__(self, pin=16):
        self.pin = pin
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
    def off(self):
        GPIO.output(self.pin, False)
        self.state = False
        syslog.syslog(syslog.LOG_INFO, "Cooling FAN - OFF")
    
    def on(self):
        GPIO.output(self.pin, True)
        self.state = True
        syslog.syslog(syslog.LOG_INFO, "Cooling FAN - ON")
    
    def is_on(self):
        return self.state


class cpu_monitor():

    def __init__(self, trigger_temp=60, buffer=5):
        self.trigger_temp = trigger_temp
        self.temp = self._temp()
        self.temperatures = [self.temp for i in range(buffer)]
        
    def _temp(self):
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if not stderr:
            stdout = stdout.decode("utf-8") 
            temp = stdout[(stdout.find('=')+1):-3]  #Extract value from '=' sign to 3rd character from the end
            return float(temp)
        else:
            return self.trigger_temp

    def update(self):
        self.temperatures.pop(0)
        self.temperatures.append(self._temp())
        self.temp = sum(self.temperatures) / len(self.temperatures)
        return self.temp