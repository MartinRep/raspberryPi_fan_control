from subprocess import Popen, PIPE
import RPi.GPIO as GPIO 
from time import sleep
from collections import deque
import getopt
import sys

class fan_control():
    
    def __init__(self, pin=16):
        self.pin = pin
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
    def off(self):
        GPIO.output(self.pin, False)
        self.state = False
    
    def on(self):
        GPIO.output(self.pin, True)
        self.state = True
    
    def is_on(self):
        return self.state


class cpu_monitor():

    def __init__(self, trigger_temp=60, delay=5):
        self.trigger_temp = trigger_temp
        self.temp = self._temp()
        self.temperatures = [self.temp for i in range(delay)]
        
    
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
        

    
def main():
    trigger_temp = 60
    delay = 5
    pin = 16
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, 't:d:p:')
    for key, value in opts:
        if(key is 't'):
            trigger_temp = value
        if(key is 'd'):
            delay = value
        if(key is 'p'):
            pin = value
    fan = fan_control(pin)
    monitor = cpu_monitor(trigger_temp=trigger_temp, delay=delay)
    while True:
        if(monitor.update() > trigger_temp):
            fan.on()
        else:
            fan.off()
        sleep(1)


if __name__ == "__main__":
    main()
