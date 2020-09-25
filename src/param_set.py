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


################################################################################
# Classes
class ParamSet:

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the ParamSet class
    # @param    module      module file name
    # @param    main_dir    main directory, root directory
    # @return   none
    ############################################################################
    def __init__(self, set_name='.sets', param_dir='param'):
        print('parameter file: ', set_name)
        print('parameter file folder: ', param_dir)
        self.set_name = set_name
        self.param_dir = param_dir


        #self.wifi_ssid = 'your ssid'
        #self.wifi_pwd = 'your pwd'

    ############################################################################
    # @brief    get WIFI ssid parameter
    # @return   returns the wifi ssid
    ############################################################################
    def get_wifi_ssid(self):
        return(self.wifi_ssid)

    ############################################################################
    # @brief    get WIFI ssid parameter
    # @return   returns the wifi password
    ############################################################################
    def get_wifi_password(self):
        return(self.wifi_pwd)
