################################################################################
# filename: clean_sources.py
# date: 03. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module initiales the parameter sets in the file system.
# known devices:
#   1. [0x58, 0x2d, 0x34, 0x38, 0x64, 0x37]
#   2. [0x58, 0x2D, 0x34, 0x37, 0x10, 0x86]
#   3. [0x58, 0x2D, 0x34, 0x39, 0x16, 0xa7]
#   4. [0x58, 0x2D, 0x34, 0x3b, 0x8c, 0x66]
#   4. [0xa4, 0xC1, 0x38, 0x2E, 0x8d, 0x23]
################################################################################

################################################################################
# Imports
import time
import src.utils.trace as T
from src.utils.ble_drv import BleListener
from src.utils.ble_drv import ble_append_listener
from src.utils.ble_drv import ble_remove_listener

################################################################################
# Functions
################################################################################
# @brief    This function is used for the check as callback
#           scanner
# @param    addr_type   type of address
# @param    addr        source address of the message
# @param    adv_type    data type of the message
# @param    rssi        rssi
# @param    adv_data    payload of the message or the message itself
# @return   none
################################################################################
def _check_callback(addr_type, addr, adv_type, rssi, adv_data):
    if((0x95 == adv_data[5]) and (0xFE == adv_data[6])):
        T.trace(__name__, T.DEBUG, '--- DEVICE found:-----------------------------')
        T.trace(__name__, T.DEBUG, 'addr :' + ' '.join('{:02x}'.format(x) for x in addr))
        T.trace(__name__, T.DEBUG, 'rssi: ' + str(rssi))
        T.trace(__name__, T.DEBUG, 'adv_data: ')
        T.trace(__name__, T.DEBUG, ' '.join('{:02x}'.format(x) for x in adv_data))
        T.trace(__name__, T.DEBUG, '----------------------------------------------')

################################################################################
# Classes
    ############################################################################
    # Member Variables
    ############################################################################
    # Member Functions

################################################################################
# Scripts
T.configure(__name__, T.DEBUG)

if __name__ == "__main__":
    print('--- search for mija devices script ---')
    filter = BleListener("ALL", _check_callback)
    #filter = BleListener("NEW", _check_callback, bytearray([0xa4, 0xc1, 0x38, 0x2e, 0x8d, 0x23]))
    ble_append_listener(filter)
    time.sleep(30)
    ble_remove_listener(filter)
