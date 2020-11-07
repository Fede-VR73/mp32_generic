################################################################################
# filename: user_blue.py
# date: 03. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module handles the bluetooth devices.
################################################################################

################################################################################
# Imports

import bluetooth
import random
import struct
import time
import micropython
from micropython import const

################################################################################
# Variables
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)

_NONE_FILTER = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

_central = None

################################################################################
# Functions

################################################################################
# @brief    This function starts the bluetppth scanner service.
# @return   none
################################################################################
def ble_drv_start():
    global _central
    print('start the bluetooth driver')
    ble = bluetooth.BLE()
    _central = BleDriver(ble)
    _central.scan_for_devices()

################################################################################
# @brief    This function stops the bluetooth scanner service
# @return   none
################################################################################
def ble_drv_stop():
    global _central
    print('stop the bluetooth driver')
    _central.stop_scan()

################################################################################
# @brief    This function appends a listener object to get notified if a message
#               from a dedicated source arrives
# @param    filter   filter mask and callback function objects
# @return   none
################################################################################
def ble_append_listener(filter):
    global _central
    print('append filter: ' + str(filter))
    _central.append_listener(filter)

################################################################################
# @brief    This function is used for the internal test scripting as callback
#           scanner
# @param    addr_type   type of address
# @param    addr        source address of the message
# @param    adv_type    data type of the message
# @param    rssi        rssi
# @param    adv_data    payload of the message or the message itself
# @return   none
################################################################################
def _test_callback(addr_type, addr, adv_type, rssi, adv_data):
    print('--- MIJA found:-------------------------------')
    print('addr_type: ' + str(addr_type))
    print('addr :')
    print(' '.join('{:02x}'.format(x) for x in addr))
    print('adv_type: ' + str(adv_type))
    print('rssi: ' + str(rssi))
    print('adv_data: ')
    print(' '.join('{:02x}'.format(x) for x in adv_data))

################################################################################
# Classes

################################################################################
# @brief    This class defines the bluetooth driver scan handler
################################################################################
class BleDriver:

    ############################################################################
    # Member Variables
    _ble = None
    _filter = []

    ############################################################################
    # Member Functions
    ############################################################################
    # @brief    constructor of the BleDriver class
    # @param    ble     bluetppth object
    # @return   none
    ############################################################################
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._filter = []

    ############################################################################
    # @brief    This function stops the scan process
    # @return   none
    ############################################################################
    def stop_scan(self):
        self._ble.gap_scan(None, 30000, 30000, False)

    ############################################################################
    # @brief    This function allows the appending of listener objects to listen
    #           to dedicated messages
    # @param    ble     bluetppth object
    # @return   none
    ############################################################################
    def append_listener(self, filter):
        self._filter.append(filter)

    ############################################################################
    # @brief    This function is the callback for a received scan result
    # @param    event     bluetooth driver event signal
    # @param    data      bluetooth message
    # @return   none
    ############################################################################
    def _ble_scanner_irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            for obj in self._filter:
                if obj.compare(addr):
                    obj.msg_callback(addr_type, addr, adv_type, rssi, adv_data)
        elif event == _IRQ_SCAN_DONE:
            print("_IRQ_SCAN_DONE")

    ############################################################################
    # @brief    This function starts the scan process
    # @return   none
    ############################################################################
    def scan_for_devices(self):
        self.stop_scan()
        self._addr_type = None
        self._addr = None
        self._ble.irq(self._ble_scanner_irq)
        #self._ble.gap_scan(10000, 500000, 500000, False)
        self._ble.gap_scan(0, 500000, 500000, False)

################################################################################
# @brief    This class defines the listener object for the bluetooth driver
#               scanner
################################################################################
class BleListener:

    ############################################################################
    # Member Functions
    ############################################################################
    # @brief    constructor of the BleListener class
    # @param    name            name of the listener
    # @param    msg_callback    callback function if message arrives
    # @param    addr_filter     optional filter, no filter object cause all
    #                           messages to be passed to the callback
    # @return   none
    ############################################################################
    def __init__(self, name, msg_callback, addr_filter = _NONE_FILTER):
        self.name = name
        self.addr_filter = addr_filter
        self.msg_callback = msg_callback

    ############################################################################
    # @brief    compare function for the recieved message base on the address
    # @param    addr            received address
    # @return   true if the addresses matches or the default address is set,
    #           else false
    ############################################################################
    def compare(self, addr):
        if((self.addr_filter == addr) or (self.addr_filter == _NONE_FILTER)):
            return True
        else:
            return False

################################################################################
# Scripts
if __name__ == "__main__":
    print('--- ble_driver script -------')
    ble_drv_start()
    filter = BleListener("Badezimmer oben", _test_callback, bytearray([0x58, 0x2d, 0x34, 0x38, 0x64, 0x37]))
    ble_append_listener(filter)
    filter2 = BleListener("Badezimmer unten", _test_callback, bytearray([0x58, 0x2D, 0x34, 0x37, 0x10, 0x86]))
    ble_append_listener(filter2)
    filter3 = BleListener("ALL", _test_callback)
    ble_append_listener(filter3)
    time.sleep(5)
    ble_drv_stop()
