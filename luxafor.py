#!/bin/python3

"""
Controls an USB Luxafor signal light from python.

"""

import usb.core

__author__ = "Tommy van Schie"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Tommy van Schie"
__email__ = "tommy@vschie.eu"


DEVICE_PID = 0xf372;
DEVICE_VID = 0x04d8;

DEVICE_COMMAND_COLOR_PREDEF = 0x00
DEVICE_COMMAND_COLOR_CODE = 0x01
DEVICE_COMMAND_FLASH = 0x03
DEVICE_COMMAND_WAVE = 0x04
DEVICE_COMMAND_ANIMATE = 0x06

WAVE_SHORT = 0x01;
WAVE_LONG = 0x02;
WAVE_SHORT_OVERLAPPING = 0x03;
WAVE_LONG_OVERLAPPING = 0x04;

# ANIMATE 0x01..0x08
ANIMATE_TRAFFICLIGHT=0x01
ANIMATE_FADE=0x04
ANIMATE_POLICE=0x05
ANIMATE_FLASH=0x07
ANIMATE_RAINBOW=0x08

COLOR_CODES = {'green': 71, 'yellow': 89, 'red': 82, 'blue': 66, 'white': 87, 'off': 79}

TARGET_ALL=0xFF

class LuxaFor():
    _device: None

    def __init__(self, idVendor=DEVICE_VID, idProduct=DEVICE_PID):
        self._device = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        if self._device is None:
            raise Exception('Cannot find device.')

        try:
            self._device.detach_kernel_driver(0)
        except usb.core.USBError:
            pass

        try:
            self._device.set_configuration()
        except usb.core.USBError:
            raise Exception('Cannot configure device, did you give Luxafor USB permission to your user?')

        self._device.set_configuration()

    @staticmethod
    def _resolve_color(color):
        cc = color.lstrip('#')
        lv = len(cc)
        return tuple(int(cc[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def _reset_device(self):
        self._device.write(1, [0, 0])

    def _write_device(self, command, *options):
        data = [command]
        for option in options:
            data.append(option)
        self._device.write(1, data)

    def set_color(self, color_rgb_code="#FFFFFF"):
        [r,g,b] = self._resolve_color(color_rgb_code)
        self._write_device(DEVICE_COMMAND_COLOR_CODE, TARGET_ALL, r,g,b, 0,0,0)

    def predefined_color(self, color='red'):
        self._write_device(DEVICE_COMMAND_COLOR_PREDEF, COLOR_CODES[color.lower()])

    def animate(self, animation_type=ANIMATE_TRAFFICLIGHT, repeat=10):
        self._write_device(DEVICE_COMMAND_ANIMATE, animation_type, repeat)

    def animate_trafficLight(self, repeat=10):
        self.animate(ANIMATE_TRAFFICLIGHT, repeat)
    def animate_fade(self, repeat=10):
        self.animate(ANIMATE_FADE, repeat)
    def animate_police(self, repeat=10):
        self.animate(ANIMATE_POLICE, repeat)
    def animate_flash(self, repeat=10):
        self.animate(ANIMATE_FLASH, repeat)
    def animate_rainbow(self, repeat=10):
        self.animate(ANIMATE_RAINBOW, repeat)


    def wave(self, color, wave_type=WAVE_SHORT, repeat=5, speed=5):
        [r,g,b] = self._resolve_color(color)
        self._write_device(DEVICE_COMMAND_WAVE, wave_type, r,g,b, 0x00, repeat, speed)

    def flash(dev, color, target=0xff, speed=20, repeat=5):
        [r,g,b] = self._resolve_color(color)
        self._write_device(DEVICE_COMMAND_FLASH, TARGET_ALL, speed, 0x00, repeat)


