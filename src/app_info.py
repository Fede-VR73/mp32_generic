################################################################################
# filename: app_info.py
# date: 06. Oct. 2020
# username: winkste
# name: Stephan Wink
# description: This module controls the version information and the application
#identification string as well as a short description.

################################################################################

################################################################################
# Imports
import os

################################################################################
# Variables

################################################################################
# Classes

class AppInfo:

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the AppInfo object
    # @return   none
    ############################################################################
    def __init__(self):
        self.partnumber = 'N39005'
        self.qualifier = 'TC'
        self.version ='0.0.0'
        self.description = 'This is a micropython test project for ESP32 devices'

        self.__get_local_version()

    ############################################################################
    # @brief    Returns the version of the current installed firmware
    # @param    directory   directory of the version file
    # @param    version_file_name   file name with the content of actual version
    # @return   none
    ############################################################################
    def __get_local_version(self, directory='src', version_file_name='.version'):
        try:
            version_file_name in os.listdir(directory)
            f = open(directory + '/' + version_file_name)
            self.version = f.read()
            f.close()
        except OSError:
            self.version = '0.0.0'

    ############################################################################
    # @brief    prints the complete partnumber string
    # @return   none
    ############################################################################
    def print_partnumber(self):
        print('Firmware Partnumber: ', self.partnumber, self.qualifier, self.version)
################################################################################
# Methods
