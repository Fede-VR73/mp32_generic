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
from src.ota_updater import download_and_install_update_if_available
from src.param_set import ParamSet
from src.user_pins import UserPins
from src.mqtt.user_mqtt import start_mqtt_client
from src.app_info import AppInfo
import esp
import network
import src.trace as T

################################################################################
# Variables
repl_mode = False
mqtt_client = None

################################################################################
# Methods

################################################################################
# @brief    initialize the network and connect to WLAN
# @param    ssid        the ssid of the station to connect to
# @param    password    the password to connect tot the wifi station
# @return   none
################################################################################
def connect_to_wifi_network(ssid, password):

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        T.trace(__name__, T.DEBUG, 'connecting to network...')
        sta_if.active(True)
        T.trace(__name__, T.DEBUG, ssid)
        T.trace(__name__, T.DEBUG, password)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    T.trace(__name__, T.DEBUG, 'network config:' + str(sta_if.ifconfig()))

################################################################################
# @brief    user boot function
# @return   none
################################################################################
def do_user_boot():
    global repl_mode

    T.configure(__name__, T.INFO)
    T.trace(__name__, T.DEBUG, 'user boot...')
    esp.osdebug(None)

    pins = UserPins()
    pins.led_on()
    pinStateHigh = pins.sample_repl_req_low_state()
    if 50 < pinStateHigh:
        repl_mode = True
        T.trace(__name__, T.DEBUG, 'repl request detected...')
    else:
        repl_mode = False
        T.trace(__name__, T.DEBUG, 'standard user detected...')
    pins.led_off()

    T.trace(__name__, T.DEBUG, 'initialize parameter sets...')
    para = ParamSet()

    T.trace(__name__, T.DEBUG, 'print firmware identification...')
    app = AppInfo()
    app.print_partnumber()
    app.print_descrption()

    if True != repl_mode:
        T.trace(__name__, T.DEBUG, 'connect to user network...')
        connect_to_wifi_network(para.get_wifi_ssid(), para.get_wifi_password())

        T.trace(__name__, T.DEBUG, 'check for a new firmware version on github...')
        download_and_install_update_if_available(para.get_gitHub_repo())

        T.trace(__name__, T.DEBUG, 'start the webrepl...')
        import webrepl
        webrepl.start()
