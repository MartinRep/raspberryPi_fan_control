import syslog

class display:

    def __init__(self):
        try:
            self.set_brightness(self.brightness_is())
        except Exception:
            syslog.syslog(syslog.LOG_ERR, " ! Failed to access display controller ! \n !      This must be run as sudo       !")
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

