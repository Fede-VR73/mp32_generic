################################################################################
# filename: pin_cfg.py
# date: 10. Jun. 2021
# username: winkste
# name: Stephan Wink
# description: This module defines all pin assignments on one local point.
################################################################################

################################################################################
# Imports

################################################################################
# Variables
_GPIO_00        = 0
_GPIO_02        = 2
_GPIO_04        = 4
_GPIO_16        = 16
_GPIO_17        = 17
_GPIO_18        = 18
_GPIO_19        = 19
_GPIO_21        = 21
_GPIO_23        = 23
_GPIO_25        = 25
_GPIO_26        = 26
_GPIO_27        = 27
_GPIO_32        = 32
_GPIO_33        = 33
_GPIO_35        = 35

BOOT_LED_GPIO       = _GPIO_02
REPL_REQUEST_GPIO   = _GPIO_00
RELAY_OUT_GPIO      = _GPIO_21
NEO_DATA_GPIO       = _GPIO_16
DHT22_PWR_GPIO      = _GPIO_26
DHT22_DAT_GPIO      = _GPIO_25
PIR_PWR_GPIO        = _GPIO_23
PIR_DATA_GPIO       = _GPIO_17
PIR_LED_GPIO        = _GPIO_18
TEMP_PWR_GPIO       = _GPIO_32
TEMP_DAT_ADC        = _GPIO_35
SWITCH_GPIO         = _GPIO_04
SWITCH_LED_GPIO     = _GPIO_19


################################################################################
# Classes

################################################################################
# Methods
