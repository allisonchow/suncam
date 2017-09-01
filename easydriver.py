"""
EasyDriver interface code using Adafruit BBIO's GPIO code.

Converted from a RaspberryPi version by Renn.
"""


import Adafruit_BBIO.GPIO as gpio
import time
import math


class easydriver(object):   
    def __init__(self,
                 pin_step=None, delay=0.1, pin_direction=None,
                 pin_ms1=None, pin_ms2=None, pin_ms3=None,
                 pin_sleep=None, pin_enable=None, pin_reset=None,
                 name="Stepper"):

        self.pin_step = pin_step
        self.delay = delay / 2
        self.pin_direction = pin_direction  # Assume that you are using pin_direction as positive always, 0 is forward, 1 is backwards
        self.pin_microstep_1 = pin_ms1
        self.pin_microstep_2 = pin_ms2
        self.pin_microstep_3 = pin_ms3
        self.pin_sleep = pin_sleep
        self.pin_enable = pin_enable
        self.pin_reset = pin_reset
        self.name = name
        self.remainder = 0

        self.steps_taken = 0.0
        self.angle = 0

        if self.pin_step is not None:
            gpio.setup(self.pin_step, gpio.OUT)
        if self.pin_direction is not None:
            gpio.setup(self.pin_direction, gpio.OUT)
            gpio.output(self.pin_direction, True)
        if self.pin_microstep_1 is not None:
            gpio.setup(self.pin_microstep_1, gpio.OUT)
            gpio.output(self.pin_microstep_1, False)
        if self.pin_microstep_2 is not None:
            gpio.setup(self.pin_microstep_2, gpio.OUT)
            gpio.output(self.pin_microstep_2, False)
        if self.pin_microstep_3 is not None:
            gpio.setup(self.pin_microstep_3, gpio.OUT)
            gpio.output(self.pin_microstep_3, False)
        if self.pin_sleep is not None:
            gpio.setup(self.pin_sleep, gpio.OUT)
            gpio.output(self.pin_sleep, True)
        if self.pin_enable is not None:
            gpio.setup(self.pin_enable, gpio.OUT)
            gpio.output(self.pin_enable, False)
        if self.pin_reset is not None:
            gpio.setup(self.pin_reset, gpio.OUT)
            gpio.output(self.pin_reset, True)

    def step(self):
        gpio.output(self.pin_step, True)
        time.sleep(self.delay)
        gpio.output(self.pin_step, False)
        time.sleep(self.delay)

    def set_direction(self, direction):
        gpio.output(self.pin_direction, direction)

    def set_full_step(self):
        gpio.output(self.pin_microstep_1, False)
        gpio.output(self.pin_microstep_2, False)
        gpio.output(self.pin_microstep_3, False)

    def set_half_step(self):
        gpio.output(self.pin_microstep_1, True)
        gpio.output(self.pin_microstep_2, False)
        gpio.output(self.pin_microstep_3, False)

    def set_quarter_step(self):
        gpio.output(self.pin_microstep_1, False)
        gpio.output(self.pin_microstep_2, True)
        gpio.output(self.pin_microstep_3, False)

    def set_eighth_step(self):
        gpio.output(self.pin_microstep_1, True)
        gpio.output(self.pin_microstep_2, True)
        gpio.output(self.pin_microstep_3, False)

    def set_sixteenth_step(self):
        gpio.output(self.pin_microstep_1, True)
        gpio.output(self.pin_microstep_2, True)
        gpio.output(self.pin_microstep_3, True)

    def sleep(self):    
        gpio.output(self.pin_sleep, False)

    def wake(self):
        gpio.output(self.pin_sleep, True)

    def disable(self):
        gpio.output(self.pin_enable, True)

    def enable(self):
        gpio.output(self.pin_enable, False)

    def reset(self):
        gpio.output(self.pin_reset, False)
        time.sleep(1)
        gpio.output(self.pin_reset, True)

    def set_delay(self, delay):
        self.delay = delay / 2

    def rotate(self, angle_needed):
        steps_taken = 0
        steps_per_rev = 400.0 * 16.0
        angle_per_step = 360.0 / steps_per_rev

        steps_needed = round(angle_needed / angle_per_step)
        d_angle = steps_needed * angle_per_step

        print 'rotating!'

        gpio.setup(self.pin_direction, gpio.OUT)
        gpio.output(self.pin_direction, True)

        if angle_needed > 0:
            gpio.setup(self.pin_direction, gpio.OUT)
            gpio.output(self.pin_direction, False)

        while steps_taken < steps_needed:
            self.step()
            steps_taken += 1
            time.sleep(self.delay)

        return d_angle

    def finish(self):
        gpio.cleanup()
