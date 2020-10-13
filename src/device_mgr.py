################################################################################
# filename: device_mgr.py
# date: 11. Oct. 2020
# username: winkste
# name: Stephan Wink
# description: This module controls all possible device configurations
#
################################################################################

################################################################################
# Imports

################################################################################
# Variables

################################################################################
# Functions
################################################################################
# @brief    Initializes and starts the device manager
# @param    id       device id
# @param    cap      capability
# @return   none
################################################################################
def start_device_manager(id, cap):
    print("device manager started...")

################################################################################
# @brief    Executes the configured devices
# @return   none
################################################################################
def stop_device_manager():
    print("device manager stopped...")

################################################################################
# @brief    Stops the device manager
# @return   none
################################################################################
def execute_devices():
    print("executes the devices...")

################################################################################
# Classes

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    start_device_manager("dev01", 0x20)
    execute_devices()
    stop_device_manager()
