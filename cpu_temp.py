from subprocess import Popen, PIPE
import RPi.GPIO as GPIO 
from time import sleep
from collections import deque

class fan_control():
    
    def __init__(self, pin):
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

    def __init__(self):
        temp = cpu_monitor.get_temp()
        self.temperatures = [temp, temp, temp, temp, temp, temp, temp, temp, temp, temp]
    
    @staticmethod
    def get_temp():
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8") 
        temp = stdout[(stdout.find('=')+1):-3]  #Extract value from '=' sign to 3rd character from the end
        return float(temp)

    def update(self):
        self.temperatures.pop(0)
        self.temperatures.append(cpu_monitor.get_temp())
    
    def average_temp(self):
        temp_sum = 0
        for temp in self.temperatures:
            temp_sum += temp
        return temp_sum / len(self.temperatures)

    
def main():
    fan = fan_control(16)
    monitor = cpu_monitor()
    while True:
        monitor.update()
        print(f"Average temperature: {monitor.average_temp()} 'C")
        if(monitor.average_temp() > 60):
            fan.on()
        else:
            fan.off()
        sleep(1)


if __name__ == "__main__":
    main()

