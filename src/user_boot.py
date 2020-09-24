################################################################################
# filename: user_boot.py
# date: 23. Sept. 2020
# username: winkste
# name: Stephan Wink
# description: This module is the local project dependent boot module. It is
# expected to be called within the standard boot file in the root directory.

################################################################################

################################################################################
# Imports
from time import sleep
from machine import Pin

################################################################################
# Methods

################################################################################
# @brief    blink once the onboard LED
# @return   none
################################################################################
def blink_once():
    led = Pin(2, Pin.OUT) # defines output pin 5 for on board LED
    led.on()
    sleep(1)
    led.off()
    sleep(1)

################################################################################
# @brief    blinks loop_count times the onboard LED
# @param    loop_count count of expected blinks
# @return   none
################################################################################
def user_blink(loop_count):
    i = 1
    while i < loop_count:
        blink_once()
        i = i + 1

################################################################################
# @brief    at start blink once to indicate chip is up and running
# @return   none
################################################################################
def start_blink():
    blink_once()

################################################################################
# @brief    after network connection initialization, blink twice
# @return   none
################################################################################
def network_blink():
    blink_once()
    blink_once()

################################################################################
# @brief    initialize the network and connect to WLAN
# @return   none
################################################################################
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('FRITZ!Box 7580 RU', '84757589397899114157')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

################################################################################
# @brief    user boot function
# @return   none
################################################################################
def do_user_boot():
    print('user boot...')
    start_blink()
    print('connect to user network...')
    do_connect()
    network_blink()

    import webrepl
    webrepl.start()
