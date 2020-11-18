################################################################################
# filename: boot_pins.py
# date: 23. Sept. 2020
# username: winkste
# name: Stephan Wink
# description: This module controls the boot and startup LED indicator and the
# user request repl start.

################################################################################

################################################################################
# Imports
from time import sleep
from machine import Pin

################################################################################
# Classes
class UserPins:

        ############################################################################
        # Member Functions

        ############################################################################
        # @brief    constructor of the UserPins object
        # @return   none
        ############################################################################
        def __init__(self):
            self.repl_req_pin = Pin(0, Pin.IN) # defines the button to repl request
            self.led = Pin(2, Pin.OUT) # defines output pin 5 for on board LED


        ################################################################################
        # @brief    blink once the onboard LED for 1 second
        # @return   none
        ################################################################################
        def led_blink_one_second(self):
            self.led.on()
            sleep(1)
            self.led.off()
            sleep(1)

        ################################################################################
        # @brief    turn led on
        # @return   none
        ################################################################################
        def led_on(self):
            self.led.on()

        ################################################################################
        # @brief    turn led off
        # @return   none
        ################################################################################
        def led_off(self):
            self.led.off()

        ################################################################################
        # @brief    blinks loop_count times the onboard LED
        # @param    loop_count count of expected blinks
        # @return   none
        ################################################################################
        def led_blink(self, loop_count):
            i = 1
            while i < loop_count:
                self.led_blink_one_second()
                i = i + 1

        ################################################################################
        # @brief    samples the low state of the repl request pin for a dedicated
        #           sample time
        # @param    sample_time_ms     sample time in milliseconds
        # @param    sample_rate_ms     sample rate in milliseconds
        # @return   none
        ################################################################################
        def sample_repl_req_low_state(self, sample_time_ms=2000, sample_rate_ms=10):
            i = 1
            count = 0

            while i < sample_time_ms:
                if(0 == self.repl_req_pin.value()):
                    count = count + 1
                i = i + sample_rate_ms
                sleep(sample_rate_ms / 1000.0)
            return count
