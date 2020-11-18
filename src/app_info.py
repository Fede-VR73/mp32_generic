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
import src.trace as T

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

        T.configure(__name__, T.INFO)
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
        complete_pn = self.partnumber + self.qualifier + self.version
        T.trace(__name__, T.INFO, 'Firmware Partnumber: ' + complete_pn)

    ############################################################################
    # @brief    Getter function for the firmware identifier
    # @return   the firmware identification string
    ############################################################################
    def get_fw_identifier(self):
        fw_ident = self.partnumber + self.qualifier
        return fw_ident

    ############################################################################
    # @brief    Getter function for the firmware version
    # @return   the firmware version
    ############################################################################
    def get_fw_version(self):
        return self.version

    ############################################################################
    # @brief    prints the description string of the application
    # @return   none
    ############################################################################
    def print_descrption(self):
        T.trace(__name__, T.DEBUG, 'Firmware Description: ' + self.description)

    ############################################################################
    # @brief    Getter function for the firmware description
    # @return   the description string of the application
    ############################################################################
    def get_description(self):
        return self.description


################################################################################
# Methods
