################################################################################
# filename: hw_test.py
# date: 10. Jan. 2021
# username: winkste
# name: Stephan Wink
# description: This module provides hardware function tests for connected
#               peripherie.
################################################################################

################################################################################
# Imports
from time import sleep
from machine import Pin
################################################################################
# Variables

_GPIO_0         = 0
_GPIO_2         = 2
_GPIO_25        = 25
_GPIO_26        = 26
_GPIO_27        = 27
_GPIO_33        = 33
_GPIO_32        = 32
_GPIO_35        = 35
_GPIO_17        = 17
_GPIO_21        = 21
_GPIO_18        = 18
_GPIO_19        = 19
_GPIO_16        = 16
_GPIO_23        = 23

#input pins
_LED2_GPIO      = _GPIO_2
_LED18_GPIO     = _GPIO_18
_LED19_GPIO     = _GPIO_19
_LED21_GPIO     = _GPIO_21
_NEO_DATA_GPIO  = _GPIO_16
_DHT22_PWR_GPIO = _GPIO_26
_PIR_PWR_GPIO   = _GPIO_23
_TEMT_PWR_GPIO  = _GPIO_32

#output pins
_SWITCH0_GPIO   = _GPIO_0
_DHT22_DAT_GPIO = _GPIO_25
_PIR_DATA_GPIO  = _GPIO_17

#ADC pins
_TEMP_DAT_ADC   = _GPIO_32

#################################################################################
# Functions
################################################################################
# @brief    This function tests LED2
# @return   none
################################################################################
def test_led2():
    _test_output_pin(_LED2_GPIO)

################################################################################
# @brief    This function tests LED18
# @return   none
################################################################################
def test_led18():
    _test_output_pin(_LED18_GPIO)

################################################################################
# @brief    This function tests LED19
# @return   none
################################################################################
def test_led19():
    _test_output_pin(_LED19_GPIO)

################################################################################
# @brief    This function tests LED21
# @return   none
################################################################################
def test_led21():
    _test_output_pin(_LED21_GPIO)

################################################################################
# @brief    This function tests the neo data output pin
# @return   none
################################################################################
def test_neo_data():
    _test_output_pin(_NEO_DATA_GPIO)

################################################################################
# @brief    This function tests the DHT22 power pin
# @return   none
################################################################################
def test_dht_pwr():
    _test_output_pin(_DHT22_PWR_GPIO)

################################################################################
# @brief    This function tests the PIR power pin
# @return   none
################################################################################
def test_pir_pwr():
    _test_output_pin(_PIR_PWR_GPIO)

################################################################################
# @brief    This function tests the TEMT6000 power pin
# @return   none
################################################################################
def test_temt_pwr():
    _test_output_pin(_TEMT_PWR_GPIO)

################################################################################
# @brief    This function tests an output pin
# @param    pin_nr      pin number
# @return   none
################################################################################
def _test_output_pin(pin_nr):
    gpio = Pin(pin_nr, Pin.OUT)
    for i in range(0,5):
        gpio.off()
        sleep(1)
        gpio.on()
        sleep(1)
    gpio.off()

################################################################################
# @brief    This function tests the switch 0 input pin
# @return   none
################################################################################
def test_switch0():
    _test_input_pin(_SWITCH0_GPIO)

################################################################################
# @brief    This function tests the DHT22 data input pin
# @return   none
################################################################################
def test_dht_data():
    _test_input_pin(_DHT22_DAT_GPIO)

################################################################################
# @brief    This function tests the PIR data input pin
# @return   none
################################################################################
def test_pir_data():
    _test_input_pin(_PIR_DATA_GPIO)

################################################################################
# @brief    This function tests the input pin
# @param    pin_nr      pin number
# @return   none
################################################################################
def _test_input_pin(pin_nr):
    gpio = Pin(pin_nr, Pin.IN)
    low = 0
    high = 0

    for i in range(0, 500):
        if(0 == gpio.value()):
            low = low + 1
        else:
            high = high + 1
        sleep(10 / 1000.0)
    print('Pin low states: ' + str(low))
    print('Pin high states: ' + str(high))

################################################################################
# Classes
    ############################################################################
    # Member Variables
    ############################################################################
    # Member Functions

################################################################################
# Scripts
if __name__ == "__main__":
    print('--- hardware test script ---')
