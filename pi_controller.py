import sys
import getopt
import syslog
from Pi_controllers import temp_ctr, disp_ctr

def print_help():
    print("     Pi Controller. \n This is help printout...")

def main():
    disp = disp_ctr.display()
    temp = temp_ctr.cpu_monitor()
    fan = temp_ctr.fan_control()
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "b:ps", ["brightness=", "power", "status"])
    except Exception as e:
        print_help()
        print(e.args[0])
        exit(1)
    for key, value in opts:
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