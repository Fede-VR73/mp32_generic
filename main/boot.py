from time import sleep
from machine import Pin
from main.ota_updater import OTAUpdater

def download_and_install_update_if_available():
    o = OTAUpdater('url-to-your-github-project')
    o.download_and_install_update_if_available('FRITZ!Box 7580 RU', '84757589397899114157')

def blink_once():
    led = Pin(2, Pin.OUT) # defines output pin 5 for on board LED
    led.on()
    sleep(1)
    led.off()
    sleep(1)

def user_blink(loop_count):
    i = 1
    while i < loop_count:
        blink_once()
        i = i + 1

def start_blink():
    blink_once()

def network_blink():
    blink_once()
    blink_once()



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

print('starting user boot...')
start_blink()
sleep(1)
print('check for new firmware version in github...')
download_and_install_update_if_available()
sleep(5)
print('connect to user network...')
do_connect()
network_blink()

import webrepl
webrepl.start()
