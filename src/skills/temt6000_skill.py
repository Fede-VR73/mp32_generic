################################################################################
# filename: temt6000_skill.py
# date: 19. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module generates the themt 6000 skill for the TEMT6000 light
#               sensor. The sensor is connected to an analog input and powered
#               via a digital output pin.
#
################################################################################

################################################################################
# Imports
import time
from src.skills.abs_skill import AbstractSkill
from src.mqtt.user_subs import UserSubs
from src.mqtt.user_pubs import UserPubs
import dht
import machine
import src.trace as T
import math

################################################################################
# Variables

################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This is the DHT skill, handling DHT sensor data
################################################################################
class Temt6000Skill(AbstractSkill):

    ############################################################################
    # Member Attributes
    _pub_brightness = None
    _pub_bright_level = None
    EXECUTION_PERIOD = 1000
    _PUB_THRESHOLD = 10.0
    _DARK_LEVEL = 300
    _ON = 1
    _OFF = 0

    _adc_pin = 0
    _adc_chan = None
    _pwr_pin = None


    _brightness = 0.0
    _last_brightness = 999.0
    _DARK = 'DARK'
    _BRIGTH = 'BRIGHT'
    _bright_level = _DARK

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the TEMT6000 skill object
    # @param    dev_id          device identification
    # @param    skill_entity    skill entity if multiple skills are generated
    # @param    adc_pin         data pin selection
    # @param    pwr_pin         power pin of the DHT, default = None
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity, adc_pin, pwr_pin=None):
        super().__init__(dev_id, skill_entity)
        self._skill_name = "DHT skill"
        self._pub_brightness = UserPubs("temt6000/raw", dev_id)
        self._pub_bright_level = UserPubs("temt6000/level", dev_id)
        self._adc_pin = data_pin
        self._pwr_pin = pwr_pin
        self._brightness = 0.0
        self._last_brightness = 999.0
        self._bright_level = _DARK


    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        if self._adc_chan == None:
            self._adc_chan = machine.ADC(self._adc_pin)

    ############################################################################
    # @brief    poweres the temt6000 chip
    # @return   none
    ############################################################################
    def _heating(self):
        T.trace(__name__, T.DEBUG, 'heating...')
        self._activate_chip()
        self._state = _MEASURE

    ############################################################################
    # @brief    measure brightness and bright level
    # @return   none
    ############################################################################
    def _measure(self):
        T.trace(__name__, T.DEBUG, 'measure...')
        self._state = _PUBLISH
        self._brightness = self._adc_chan.read()
        self._deactivate_chip()
        if(self._brightness < self._DARK_LEVEL):
            self._bright_level = self._DARK
        else:
            self._bright_level = self._BRIGTH

    ############################################################################
    # @brief    power on the chip
    # @return   none
    ############################################################################
    def _activate_chip(self):
        T.trace(__name__, T.DEBUG, 'power on...')
        if(self._pwr_pin != None):
            pin.value(self._ON)

    ############################################################################
    # @brief    power off the chip
    # @return   none
    ############################################################################
    def _deactivate_chip(self):
        T.trace(__name__, T.DEBUG, 'power off...')
        if(self._pwr_pin != None):
            pin.value(self._OFF)

    ############################################################################
    # @brief    publishes brightness and bright level
    # @return   none
    ############################################################################
    def _publish(self):
        T.trace(__name__, T.DEBUG, 'publish...')
        self._state = _HEATUP
        if math.fabs(self._last_brightness - self._brightness) > self._PUB_THRESHOLD:
            self._pub_brightness.publish(str(self._brightness))
            self._pub_bright_level.publish(self._bright_level)

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
        current_time = time.ticks_ms()
        if abs(time.ticks_diff(current_time, self._last_time)) > self.EXECUTION_PERIOD:
            self._last_time = current_time

            if(self._STATE_HEATUP == self._state):
                self._heating()
            elif(self._STATE_MEASURE == self._state):
                self._measure()
            elif(self._STATE_PUBLISH == self._state):
                self._publish()
            else:
                T.trace(__name__, T.ERROR, 'unexpected state detected')
                self._state = _STATE_HEATUP

    ############################################################################
    # @brief    executes the incoming subscription callback handler
    # @param    topic       topic identifier of the messsage
    # @param    payload     payload of the message
    # @return   none
    ############################################################################
    def execute_subscription(self, topic, data):
        T.trace(__name__, T.ERROR, 'unexpected subscription')

    ############################################################################
    # @brief    stopps the skill
    # @return   none
    ############################################################################
    def stop_skill(self):
        super().stop_skill()
        self._dht = None
        self._temperature = 0.0
        self._humidity = 0.0

################################################################################
# Scripts
T.configure(__name__, T.DEBUG)

if __name__ == "__main__":
    # execute only if run as a script
    s = Temt6000Skill('dev01', '0', 0, None)
    s.start_skill()
    time.sleep(1)
    s.execute_skill()
    time.sleep(1)
    s.execute_skill()
    time.sleep(1)
    s.execute_skill()
    s.stop_skill()
