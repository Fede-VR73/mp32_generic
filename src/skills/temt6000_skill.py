################################################################################
# filename: temt6000_skill.py
# date: 19. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module generates the themt 6000 skill for the TEMT6000 light
#               sensor. The sensor is connected to an analog input and powered
#               via a digital output pin.
#
# TODO's: How to handle averaging and what algorithm?
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
    EXECUTION_PERIOD = 500
    _SLEEP_PERIOD = 30
    _sleep_counter = 0
    _AVERAGES_PER_CYCLE = 10
    _avg_counter = 0
    _avg_sum = 0.0
    _PUB_THRESHOLD = 2.0
    _DARK_LEVEL = 300
    _ON = 1
    _OFF = 0
    NO_VALUE = 0xff

    _STATE_HEATUP = 0
    _STATE_MEASURE = 1
    _STATE_PUBLISH = 2
    _STATE_SLEEP = 3

    _adc_pin = 0
    _adc_chan = None
    _pwr_pin = NO_VALUE
    _pwr_gpio = None


    _brightness = 0
    _last_brightness = 9999
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
    def __init__(self, dev_id, skill_entity, adc_pin, pwr_pin=NO_VALUE):
        super().__init__(dev_id, skill_entity)
        self._skill_name = "TEMT6000 skill"
        self._pub_brightness = UserPubs("temt6x/raw", dev_id, "std", skill_entity)
        self._pub_bright_level = UserPubs("temt6x/level", dev_id, "std", skill_entity)
        self._adc_pin = adc_pin
        self._pwr_pin = pwr_pin
        self._brightness = 0
        self._last_brightness = 999
        self._bright_level = self._DARK
        self._sleep_counter = self._SLEEP_PERIOD


    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        self._state = self._STATE_SLEEP
        self._sleep_counter = self._SLEEP_PERIOD
        if self._adc_pin != self.NO_VALUE:
            self._adc_chan = machine.ADC(machine.Pin(self._adc_pin))
        if self._pwr_pin != self.NO_VALUE:
            self._pwr_gpio = machine.Pin(self._pwr_pin, machine.Pin.OUT)
            self._pwr_gpio.off()

        self._avg_counter = 0
        self._avg_sum = 0.0


    ############################################################################
    # @brief    poweres the temt6000 chip
    # @return   none
    ############################################################################
    def _heating(self):
        T.trace(__name__, T.DEBUG, 'heating...')
        self._activate_chip()
        self._state = self._STATE_MEASURE

    ############################################################################
    # @brief    measure brightness and bright level
    # @return   none
    ############################################################################
    def _measure(self):
        T.trace(__name__, T.DEBUG, 'measure cycle: ' + str(self._avg_counter))
        if self._adc_chan != None:
            self._avg_sum = self._avg_sum + self._adc_chan.read()
        self._avg_counter = self._avg_counter + 1

        if self._avg_counter == self._AVERAGES_PER_CYCLE:
            self._brightness = int((self._avg_sum / self._avg_counter) + 0.5)
            self._avg_counter = 0
            self._avg_sum = 0.0
            self._deactivate_chip()
            if(self._brightness < self._DARK_LEVEL):
                self._bright_level = self._DARK
            else:
                self._bright_level = self._BRIGTH
            self._state = self._STATE_PUBLISH
            T.trace(__name__, T.DEBUG, 'measured brightness: ' + str(self._brightness))
            T.trace(__name__, T.DEBUG, 'last brightness: ' + str(self._last_brightness))
            T.trace(__name__, T.DEBUG, 'brightness level: ' + self._bright_level)

    ############################################################################
    # @brief    power on the chip
    # @return   none
    ############################################################################
    def _activate_chip(self):
        T.trace(__name__, T.DEBUG, 'power on...')
        if(self._pwr_gpio != None):
            self._pwr_gpio.on()

    ############################################################################
    # @brief    power off the chip
    # @return   none
    ############################################################################
    def _deactivate_chip(self):
        T.trace(__name__, T.DEBUG, 'power off...')
        if(self._pwr_gpio != None):
            self._pwr_gpio.off()

    ############################################################################
    # @brief    publishes brightness and bright level
    # @return   none
    ############################################################################
    def _publish(self):
        T.trace(__name__, T.DEBUG, 'publish...')
        self._state = self._STATE_SLEEP

        T.trace(__name__, T.DEBUG, 'math.fabs: ' + str(math.fabs(self._last_brightness - self._brightness)))
        if math.fabs(self._last_brightness - self._brightness) > self._PUB_THRESHOLD:
            self._last_brightness = self._brightness
            self._pub_brightness.publish(str(self._brightness))
            self._pub_bright_level.publish(self._bright_level)
            T.trace(__name__, T.DEBUG, 'published data...')

    ############################################################################
    # @brief    sleeps a dedicated period of time
    # @return   none
    ############################################################################
    def _sleep(self):
        self._sleep_counter = self._sleep_counter - 1
        T.trace(__name__, T.DEBUG, 'sleeping ' + str(self._sleep_counter))

        if self._sleep_counter == 0:
            self._sleep_counter = self._SLEEP_PERIOD
            self._state = self._STATE_HEATUP
            T.trace(__name__, T.DEBUG, 'wakeup... ')

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
            elif(self._STATE_SLEEP == self._state):
                self._sleep()
            else:
                T.trace(__name__, T.ERROR, 'unexpected state detected')
                self._state = self._STATE_SLEEP

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
        self._adc_chan = None
        self._deactivate_chip()
        self._pwr_gpio = None
        self._temperature = 0.0
        self._humidity = 0.0

################################################################################
# Scripts
T.configure(__name__, T.INFO)

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
