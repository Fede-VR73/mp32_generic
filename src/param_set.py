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
import os


################################################################################
# Classes
class ParamSet:

    wifi_ssid = ''
    wifi_pwd = ''

    github_repo = ''

    mqtt_id = ''
    mqtt_broker_ip = ''
    mqtt_broker_port = 1883
    mqtt_broker_user = ''
    mqtt_broker_pwd = ''

    device_id = ''
    capability = 0x01

    wifi_ssid = ''
    wifi_pwd = ''

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

        self.__read_parameter_from_file()

    ############################################################################
    # @brief    get WIFI ssid parameter
    # @return   returns the wifi ssid
    ############################################################################
    def __read_parameter_from_file(self):
        try:
            f = open('para/.sets')
            self.wifi_ssid = f.readline().replace('\n', '')
            self.wifi_pwd = f.readline().replace('\n', '')
            self.github_repo = f.readline().replace('\n', '')
            self.mqtt_id = f.readline().replace('\n', '')
            self.mqtt_broker_ip = f.readline().replace('\n', '')
            self.mqtt_broker_port = int(f.readline().replace('\n', ''))
            self.mqtt_broker_user = f.readline().replace('\n', '')
            self.mqtt_broker_pwd = f.readline().replace('\n', '')
            self.device_id = f.readline().replace('\n', '')
            self.capability = int(f.readline().replace('\n', ''))
        except OSError:
            print("parameter read error...")

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

    ############################################################################
    # @brief    get github repository url link
    # @return   returns the github repository url
    ############################################################################
    def get_gitHub_repo(self):
        return(self.github_repo)

    ############################################################################
    # @brief    get mqtt client id
    # @return   returns the mqtt client id
    ############################################################################
    def get_mqtt_client_id(self):
        return(self.mqtt_id)

    ############################################################################
    # @brief    get mqtt broker ip
    # @return   returns the mqtt client id
    ############################################################################
    def get_mqtt_broker_ip(self):
        return(self.mqtt_broker_ip)

    ############################################################################
    # @brief    get mqtt broker port
    # @return   returns the mqtt client id
    ############################################################################
    def get_mqtt_broker_port(self):
        return(self.mqtt_broker_port)

    ############################################################################
    # @brief    get mqtt user account
    # @return   returns the mqtt client id
    ############################################################################
    def get_mqtt_broker_user(self):
        return(self.mqtt_broker_user)

    ############################################################################
    # @brief    get mqtt user password
    # @return   returns the mqtt client id
    ############################################################################
    def get_mqtt_broker_pwd(self):
        return(self.mqtt_broker_pwd)

    ############################################################################
    # @brief    get device identifier
    # @return   returns the device identifier
    ############################################################################
    def get_device_id(self):
        return(self.device_id)

    ############################################################################
    # @brief    get device capability
    # @return   returns the device capability
    ############################################################################
    def get_capability(self):
        return(self.capability)

################################################################################
# Scripts
if __name__ == "__main__":
    print('--- param_set ---')
