#!/usr/bin/python3

from time import sleep
import sys
import getopt
from mqtt_connector import mqttConn
import time

class display:

    def __init__(self):
        try:
            self.set_brightness(self.brightness_is())
        except Exception:
            print(" ! Failed to access display controller ! \n !      This must be run as sudo       !")
            exit(1)

    def _bk_switch(self, value):
        with open("/sys/class/backlight/rpi_backlight/bl_power", 'w') as disp_ctr:
            disp_ctr.write(value)

    def isOn(self):
        with open("/sys/class/backlight/rpi_backlight/bl_power", 'r') as disp_ctr:
            return not int(disp_ctr.read())

    def off(self):
        self._bk_switch("1")

    def on(self):
        self._bk_switch("0")

    def flip_switch(self):
        self._bk_switch(str(int(self.isOn())))

    def brightness_is(self):
        with open("/sys/class/backlight/rpi_backlight/brightness", 'r') as disp_brigh:
            return int(disp_brigh.read())

    def set_brightness(self, value:int):
        with open("/sys/class/backlight/rpi_backlight/brightness", 'w') as disp_brigh:
            disp_brigh.write(str(value))
    
    def brightness_up(self):
        cur_value = self.brightness_is()
        new_value = 254 if cur_value + 12 > 254 else cur_value + 12
        self.set_brightness(new_value)

    def brightness_down(self):
        cur_value = self.brightness_is()
        new_value = 254 if cur_value - 12 < 0 else cur_value - 12
        self.set_brightness(new_value)

    def set_to_bright(self):
        self.on()
        self.set_brightness(250)

    def set_to_normal(self):
        self.on()
        self.set_brightness(125)

    def set_to_dimm(self):
        self.on()
        self.set_brightness(25)
        
disp = "" 

def print_help():
    print("     Display Controller. \n This is help printout...")


def process_command(cmd):
    if(cmd["id"] == "power"):
        if(cmd["value"] == "1"):
            disp.on()
        elif(cmd["value"] == "0"):
            disp.off()
        else:
            disp.flip_switch()
    elif(cmd["id"] == "brigtness"):
        value = int(cmd["value"])
        if(value > 0 and value < 255):
            disp.set_brightness(value)

def main():
    global disp
    argv = sys.argv[1:]
    disp = display()
    try:
        opts, args = getopt.getopt(argv, "b:psd", ["brightness=", "power", "status", "deamon"])
    except Exception as e:
        print_help()
        print(e.args[0])
        exit(1)
    for key, value in opts:
        if(key in ["-d", "--deamon"]):
            mqc = mqttConn(process_command)
            mqc.subscribe()
            time.sleep(3600)
            mqc.unsubscribe()
        if(key in ['-b',"--brightness"]):
            disp.set_brightness(int(value))
        if(key in ["-p", "--power"]):
            print(value.lower())
            if(value.lower() == "on"):
                disp.on()
            elif(value.lower() == "off"):
                disp.off()
            else:
                disp.flip_switch()
        if(key in ["-s", "--status"]):
            print(disp.isOn())
            print(disp.brightness_is())
        if(key in ["-h", "--help"]):
            print_help()
    
if(__name__ == "__main__"):
    main()


