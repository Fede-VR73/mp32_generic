################################################################################
# filename: mija_skill.py
# date: 08. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module handles mija sensors and implements all necessary
#               skill functions
#
#
# Example messages:
# 02 01 06 15 16 95 fe 50 20 aa 01 12 37 64 38 34 2d 58 0d 10 04 dc 00 3a 02
# 02 01 06 15 16 95 fe 50 20 aa 01 1a 37 64 38 34 2d 58 0d 10 04 dd 00 3a 02
# 02 01 06 15 16 95 fe 50 20 aa 01 1c 37 64 38 34 2d 58 0d 10 04 dd 00 3b 02
# 02 01 06 13 16 95 fe 50 20 aa 01 1f 37 64 38 34 2d 58 06 10 02 3a 02
# 02 01 06 15 16 95 fe 50 20 aa 01 21 37 64 38 34 2d 58 0d 10 04 dd 00 3a 02
# 02 01 06 13 16 95 fe 50 20 aa 01 23 37 64 38 34 2d 58 04 10 02 dd 00
#
# A message example parsed looks like:
# address:   0  1  2  3  4       5  6    7  8  9 10     11  12 13 14 15 16 17   18  19  20  21 22   23 24
# data:     02 01 06 15 16		95 fe	50 20 aa 01		8e	86 10 37 34 2d 58	0d	10	04	ce 00	b9 01
#
# with the following interpretation:
#   - UUID address 05 and 06, data always = 0x95fe
#   - message counter address: 11
#   - device mac address address: 12 - 17,
#           data reverse, means MAC address of example: 58:2D:34:37:10:86
#   - data type address: 18, types:
#                               TEMPERATURE	            0x04
#                               HUMIDITY	            0x06
#                               BATTERY	                0x0A
#                               TEMPERATURE & HUMIDITY  0x0D
#           (example shows a temperature and humidity message)
#   - length address of the data: 20 with following length in bytes known:
#                               TEMPERATURE	            2
#                               HUMIDITY	            2
#                               BATTERY	                1
#                               TEMPERATURE & HUMIDITY  4
#       (example has got a data length of 4 bytes)
#   - data: 2 byte data sets are low byte first, here the data is parsed as follows:
#           temperature raw   = 0xce00, humidity raw  = 0xb901
#           temperature conv  = 0x00ce, humidity conf = 0x01b9
#           data to float     = data conv / 10
#           temperature float = 20,6 °C, humidity     = 44,1%
#
################################################################################

################################################################################
# Imports
import time
from src.skills.abs_skill import AbstractSkill
from src.mqtt.user_subs import UserSubs
from src.mqtt.user_pubs import UserPubs
from src.ble_drv import BleListener
from src.ble_drv import ble_append_listener
from src.ble_drv import ble_remove_listener
from micropython import const
import src.ble_drv
################################################################################
# Variables

_UUID_DATA_LOW_ADR		            = const(5)
_UUID_DATA_HIGH_ADR		            = const(6)
_MSG_CNT_ADR				        = const(11)
_DEVICE_MAC_ADR                     = const(17)
_DATA_TYPE_ID_ADR				    = const(18)
_DATA_LEN_ADR					    = const(20)

_DATA_BATTERY_LOWBYTE_ADR		    = const(21)

_DATA_HUMTEMP_TEMP_LOWBYTE_ADR	    = const(21)
_DATA_HUMTEMP_TEMP_HIGHBYTE_ADR	    = const(22)
_DATA_HUMTEMP_HUM_LOWBYTE_ADR	    = const(23)
_DATA_HUMTEMP_HUM_HIGHBYTE_ADR	    = const(24)

_DATA_TEMP_LOWBYTE_ADR			    = const(21)
_DATA_TEMP_HIGHBYTE_ADR			    = const(22)

_DATA_HUM_LOWBYTE_ADR			    = const(21)
_DATA_HUM_HIGHBYTE_ADR			    = const(22)


_UUID_DATA_LOW_VAL		            = const(0x95)
_UUID_DATA_HIGH_VAL		            = const(0xFE)

_DATA_TYPE_ID_TEMPHUM			    = const(0x0D)
_DATA_TYPE_ID_BATT				    = const(0x0A)
_DATA_TYPE_ID_TEMP				    = const(0x04)
_DATA_TYPE_ID_HUM				    = const(0x06)

_DATA_LEN_BATTERY_STD			    = const(1)
_DATA_LEN_TEMP_STD				    = const(2)
_DATA_LEN_HUM_STD				    = const(2)
_DATA_LEN_TEMPHUM_STD			    = const(4)

################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This is the generic skill, handling generic features and functions
################################################################################
class MijaSkill(AbstractSkill):

    ############################################################################
    # Member Attributes
    device_info_request = None
    EXECUTION_PERIOD = 5000

    _mija_temp = None
    _mija_hum = None
    _mija_batt = None
    _mija_msg_cnt = None
    _mija_addr = None
    _mija_msg_location = None

    _uuid = 0;
    _mac_addr = bytearray(6);
    _msg_cnt = 0;
    _data_type = 0;
    _battery = 0.0;
    _temperature = 0.0;
    _humidity = 0.0;

    _location = "not defined"
    _address = bytearray()
    _listener = None

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the generic skill object
    # @param    dev_id    device identification
    # @param    skill_entity  skill entity if multiple skills are generated
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity, location, address):
        super().__init__(dev_id, skill_entity)

        self._skill_name = "mija skill"
        self._location = location
        self._address = address

        #generate all necessary subscription objects
        self.device_info_request = UserSubs(self, "mija/data", dev_id, "std", skill_entity)
        #self.device_info_request.subscribe()

        #generate all necessary publication objects
        self._mija_temp = UserPubs("mija/temp", dev_id, "std", skill_entity)
        self._mija_hum = UserPubs("mija/hum", dev_id, "std", skill_entity)
        self._mija_batt = UserPubs("mija/batt", dev_id, "std", skill_entity)
        self._mija_msg_cnt = UserPubs("mija/cnt", dev_id, "std", skill_entity)
        self._mija_addr = UserPubs("mija/addr", dev_id, "std", skill_entity)
        self._mija_msg_location = UserPubs("mija/loc", dev_id, "std", skill_entity)


    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        self._listener = src.ble_drv.BleListener(self._location, self._data_receive_cb, self._address)
        ble_append_listener(self._listener)


    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
        current_time = time.ticks_ms()
        if abs(time.ticks_diff(current_time, self._last_time)) > self.EXECUTION_PERIOD:
            self._last_time = current_time
            self._publish_sensor_data()

    ############################################################################
    # @brief    executes the incoming subscription callback handler
    # @param    topic       topic identifier of the messsage
    # @param    payload     payload of the message
    # @return   none
    ############################################################################
    def execute_subscription(self, topic, data):
        super().execute_subscription(topic, data)

    ############################################################################
    # @brief    stopps the skill
    # @return   none
    ############################################################################
    def stop_skill(self):
        super().stop_skill()
        ble_remove_listener(self._listener)

    ############################################################################
    # @brief    publishes all data retrieved recently
    # @return   none
    ############################################################################
    def _publish_sensor_data(self):
        self._mija_temp.publish(str(self._temperature))
        self._mija_hum.publish(str(self._humidity))
        self._mija_batt.publish(str(self._battery))
        self._mija_msg_cnt.publish(str(self._msg_cnt))
        self._mija_addr.publish(' '.join('{:02x}'.format(x) for x in self._mac_addr))
        self._mija_msg_location.publish(self._location)

    ############################################################################
    # @brief    This function is used for the data receive callback
    # @param    addr_type   type of address
    # @param    addr        source address of the message
    # @param    adv_type    data type of the message
    # @param    rssi        rssi
    # @param    adv_data    payload of the message or the message itself
    # @return   none
    ############################################################################
    def _data_receive_cb(self, addr_type, addr, adv_type, rssi, adv_data):
        self._parse_msg(adv_data)

    ############################################################################
    # @brief    This function parses the message data
    # @param    adv_data    payload of the message or the message itself
    # @return   none
    ############################################################################
    def _parse_msg(self, adv_data):
        #check and parse UUID
        if((_UUID_DATA_LOW_VAL == adv_data[_UUID_DATA_LOW_ADR]) and (_UUID_DATA_HIGH_VAL == adv_data[_UUID_DATA_HIGH_ADR])):
            self._uuid = adv_data[_UUID_DATA_HIGH_ADR]
            self._uuid = self._uuid << 8
            self._uuid = self._uuid + adv_data[_UUID_DATA_LOW_ADR]

        #parse the message counter
        self._msg_cnt = adv_data[_MSG_CNT_ADR]

        #parse the mac address bytearray
        #self._mac_addr = adv_data[17:11:-1]
        self._mac_addr[0] = adv_data[17]
        self._mac_addr[1] = adv_data[16]
        self._mac_addr[2] = adv_data[15]
        self._mac_addr[3] = adv_data[14]
        self._mac_addr[4] = adv_data[13]
        self._mac_addr[5] = adv_data[12]

        #parse data based on the type
        self._data_type = adv_data[_DATA_TYPE_ID_ADR]

        if(_DATA_TYPE_ID_TEMP == self._data_type):
            self._temperature = adv_data[_DATA_TEMP_HIGHBYTE_ADR]
            self._temperature = self._temperature << 8
            self._temperature = self._temperature + adv_data[_DATA_TEMP_LOWBYTE_ADR]
            self._temperature = self._temperature / 10.0

        elif(_DATA_TYPE_ID_HUM == self._data_type):
            self._humidity = adv_data[_DATA_HUM_HIGHBYTE_ADR]
            self._humidity = self._humidity << 8
            self._humidity = self._humidity + adv_data[_DATA_HUM_LOWBYTE_ADR]
            self._humidity = self._humidity / 10.0

        elif(_DATA_TYPE_ID_BATT == self._data_type):
            self._battery = adv_data[_DATA_BATTERY_LOWBYTE_ADR]

        elif(_DATA_TYPE_ID_TEMPHUM == self._data_type):
            self._temperature = adv_data[_DATA_HUMTEMP_TEMP_HIGHBYTE_ADR]
            self._temperature = self._temperature << 8
            self._temperature = self._temperature + adv_data[_DATA_HUMTEMP_TEMP_LOWBYTE_ADR]
            self._temperature = self._temperature / 10.0

            self._humidity = adv_data[_DATA_HUMTEMP_HUM_HIGHBYTE_ADR]
            self._humidity = self._humidity << 8
            self._humidity = self._humidity + adv_data[_DATA_HUMTEMP_HUM_LOWBYTE_ADR]
            self._humidity = self._humidity / 10.0

        else:
            print('unknown data type')

        self._print_data()

    ############################################################################
    # @brief    This function prints the actual data
    # @return   none
    ############################################################################
    def _print_data(self):
        print('--- Actual Data Set: ----------')
        print('UUID: ' + str(self._uuid))
        print('MAC address: ' + ' '.join('{:02x}'.format(x) for x in self._mac_addr))
        print('MSG counter: ' + str(self._msg_cnt))
        print('Data type: ' + str(self._data_type))
        print('Battery fill: ' + str(self._battery) + ' %')
        print('Temperature: ' + str(self._temperature) + ' Grad C')
        print('Humidity: ' + str(self._humidity) + ' %')

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    print('--- mija skill script ---')
    s = MijaSkill("dev01", "1", "here", bytearray([0x58, 0x2d, 0x34, 0x38, 0x64, 0x37]))
    print('start skill')
    s.start_skill()
    print('sleep')
    time.sleep(10)
    print('stop skill')
    s.stop_skill()
