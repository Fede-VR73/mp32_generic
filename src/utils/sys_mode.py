################################################################################
# filename: mode.py
# date: 23. Sept. 2020
# username: winkste
# name: Stephan Wink
# description: This module controls the mode of the application

################################################################################

################################################################################
# Imports
from time import sleep
from machine import Pin
import src.utils.trace as T

################################################################################
# Variables
_MODE_HW_START   = 0
_MODE_BOOT       = 1
_MODE_NORMAL     = 2
_MODE_REPL       = 3
_MODE_RESET      = 4

_repl_req_pin   = 0xFF
_boot_led_pin   = 0xFF

_repl_req_gpio  = None
_boot_led_gpio  = None

_current_mode   = _MODE_HW_START

################################################################################
# Functions

################################################################################
# @brief    function to test the module features
# @return   none
################################################################################
def main():

    T.configure(__name__, T.DEBUG)

    testResult = 0
    initialize_mode_module()
    goto_boot_mode()
    if is_boot_mode_active():
        T.trace(__name__, T.DEBUG, 'boot mode active...')
        testResult+=1    # = 1
    goto_normal_mode()
    if is_normal_mode_active():
        T.trace(__name__, T.DEBUG, 'normal mode active...')
        testResult+=1   # = 2
    goto_repl_mode()
    if is_repl_mode_active():
        T.trace(__name__, T.DEBUG, 'repl mode active...')
        testResult+=1    # = 3
    goto_reset_mode()
    if is_reset_mode_active():
        T.trace(__name__, T.DEBUG, 'reset mode active...')
        testResult+=1   # = 4
    if not is_boot_mode_active() or  not is_normal_mode_active() or not is_repl_mode_active():
        testResult+=1   # = 5

    # test repl mode request long by user
    initialize_mode_module(4, 2)
    goto_boot_mode()
    if True == long_check_for_repl_via_button_request():
        testResult+=1   # = 6
        goto_repl_mode()
        if is_repl_mode_active():
            testResult+= 1  # = 7
            T.trace(__name__, T.DEBUG, 'user request repl mode long ok')

    if testResult == 7:
        T.trace(__name__, T.INFO, 'test successful')
    else:
        T.trace(__name__, T.ERROR, 'test failed')




################################################################################
# @brief    initializes the mode module
# @param    repl_req_pin, input GPIO pin number for user repl request
# @param    boot_led_pin, output GPIO pin number for boot sequence indication
# @return   none
################################################################################
def initialize_mode_module(repl_req_pin=0xff, boot_led_pin=0xff):
    global _repl_req_pin, _repl_req_gpio, _boot_led_pin, _boot_led_gpio, _current_mode
    _repl_req_pin = repl_req_pin
    _boot_led_pin = boot_led_pin

    # defines the button to repl request
    if _repl_req_pin != 0xff:
        _repl_req_gpio = Pin(_repl_req_pin, Pin.IN)

    # defines output pin for on board LED
    if _boot_led_pin != 0xff:
        _boot_led_gpio = led = Pin(_boot_led_pin, Pin.OUT)

    _led_off()

    #self.repl_req_pin = Pin(4, Pin.IN) # defines the button to repl request
    #self.repl_req_pin = Pin(0, Pin.IN) # defines the button to repl request
    #self.led = Pin(2, Pin.OUT) # defines output pin 5 for on board LED

    _current_mode   = _MODE_HW_START

################################################################################
# @brief    Go to boot mode
# @return   None
################################################################################
def goto_boot_mode():
    global _current_mode
    if _MODE_HW_START == _current_mode:
        _current_mode = _MODE_BOOT
        _led_on()
        T.trace(__name__, T.DEBUG, 'goto boot mode..')

################################################################################
# @brief    is the boot mode currntly active?
# @return   True if boot mode active, else False
################################################################################
def is_boot_mode_active():
    global _current_mode
    return _MODE_BOOT == _current_mode

################################################################################
# @brief    Go to normal mode
# @return   None
################################################################################
def goto_normal_mode():
    global _current_mode
    if _MODE_BOOT == _current_mode:
        _current_mode = _MODE_NORMAL
        _led_off()
    T.trace(__name__, T.DEBUG, 'goto normal mode..')

################################################################################
# @brief    is the normal mode currntly active?
# @return   True if normal mode active, else False
################################################################################
def is_normal_mode_active():
    global _current_mode
    return _MODE_NORMAL == _current_mode

################################################################################
# @brief    Go to repl mode
# @return   None
################################################################################
def goto_repl_mode():
    global _current_mode
    _current_mode = _MODE_REPL
    T.trace(__name__, T.DEBUG, 'goto repl mode..')

################################################################################
# @brief    is the repl mode currntly active?
# @return   True if repl mode active, else False
################################################################################
def is_repl_mode_active():
    global _current_mode
    return _MODE_REPL == _current_mode

################################################################################
# @brief    Check for repl mode user request in busy waiting for a
#           longer period.
# @return   True if repl mode was requested by user, else False
################################################################################
def long_check_for_repl_via_button_request():
    pinStateHigh = _sample_repl_req_low_state()
    if 50 < pinStateHigh:
        repl_mode = True
        T.trace(__name__, T.DEBUG, 'repl request detected...')
    else:
        repl_mode = False
        T.trace(__name__, T.DEBUG, 'standard user detected...')
    return repl_mode

################################################################################
# @brief    Check for repl mode user request in busy waiting for a
#           longer period.
# @return   True if repl mode was requested by user, else False
################################################################################
def short_check_for_repl_via_button_request():
    pinStateHigh = _sample_repl_req_low_state(100)
    if 5 < pinStateHigh:
        repl_mode = True
        T.trace(__name__, T.DEBUG, 'repl request detected...')
    else:
        repl_mode = False
    return repl_mode

################################################################################
# @brief    Go to reset mode
# @return   None
################################################################################
def goto_reset_mode():
    global _current_mode
    _current_mode = _MODE_RESET
    T.trace(__name__, T.DEBUG, 'goto reset mode..')

################################################################################
# @brief    is the reset mode currntly active?
# @return   True if reset mode active, else False
################################################################################
def is_reset_mode_active():
    global _current_mode
    return _MODE_RESET == _current_mode

################################################################################
# @brief    turn led on
# @return   none
################################################################################
def _led_on():
    global _boot_led_gpio
    if None != _boot_led_gpio:
        _boot_led_gpio.on()

################################################################################
# @brief    turn led off
# @return   none
################################################################################
def _led_off():
    global _boot_led_gpio
    if None != _boot_led_gpio:
        _boot_led_gpio.off()

################################################################################
# @brief    samples the low state of the repl request pin for a dedicated
#           sample time
# @param    sample_time_ms     sample time in milliseconds
# @param    sample_rate_ms     sample rate in milliseconds
# @return   number of low states detected, 0 if gpio not initialized
################################################################################
def _sample_repl_req_low_state(sample_time_ms=2000, sample_rate_ms=10):
    global _repl_req_gpio
    i = 1
    count = 0

    if None != _repl_req_gpio:
        while i < sample_time_ms:
            if(0 == _repl_req_gpio.value()):
                count = count + 1
            i = i + sample_rate_ms
            sleep(sample_rate_ms / 1000.0)

    return count

################################################################################
# Classes

################################################################################
# Scripts
T.configure(__name__, T.INFO)

if __name__ == "__main__":
    main()
