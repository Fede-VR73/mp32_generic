################################################################################
# filename: dht_skill.py
# date: 19. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module generates the dht skill
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

################################################################################
# Variables

################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This is the DHT skill, handling DHT sensor data
################################################################################
class DhtSkill(AbstractSkill):

    ############################################################################
    # Member Attributes
    _pub_temperature = None
    _pub_humitdity = None
    EXECUTION_PERIOD = 3000
    _SLEEP_PERIOD = 5
    _sleep_counter = 0
    NO_VALUE = 0xFF

    _STATE_HEATUP = 0
    _STATE_MEASURE = 1
    _STATE_PUBLISH = 2
    _STATE_SLEEP = 3

    _data_pin = 0
    _pwr_pin = NO_VALUE
    _pwr_gpio = None
    _dht = None

    _temperature = 0.0
    _humidity = 0.0

    _TEMPERATURE_CORR_FACTOR = 1.00
    _HUMIDITY_CORR_FACTOR =    1.23

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the DHT skill object
    # @param    dev_id          device identification
    # @param    skill_entity    skill entity if multiple skills are generated
    # @param    data_pin        data pin selection
    # @param    pwr_pin         power pin of the DHT, default = NO_VALUE
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity, data_pin, pwr_pin=NO_VALUE):
        super().__init__(dev_id, skill_entity)
        self._skill_name = "DHT skill"
        self._pub_temperature = UserPubs("temp_hum/temp", dev_id)
        self._pub_humitdity = UserPubs("temp_hum/hum", dev_id)
        self._data_pin = data_pin
        self._dht = None
        self._pwr_pin = pwr_pin
        self._pwr_gpio = None

    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):

        if self._dht == None:
            self._dht = dht.DHT22(machine.Pin(self._data_pin))
        if self._pwr_pin != self.NO_VALUE:
            self._pwr_gpio = machine.Pin(self._pwr_pin, machine.Pin.OUT)
            self._pwr_gpio.off()

        self._sleep_counter = self._SLEEP_PERIOD
        self._state = self._STATE_SLEEP

    ############################################################################
    # @brief    poweres the temt6000 chip
    # @return   none
    ############################################################################
    def _heating(self):
        T.trace(__name__, T.DEBUG, 'heating...')
        self._activate_chip()
        self._state = self._STATE_MEASURE

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
    # @brief    measure tempeature and humidity
    # @return   none
    ############################################################################
    def _measure(self):
        self._state = self._STATE_PUBLISH

        T.trace(__name__, T.DEBUG, 'measureing...')
        if self._dht != None:
            try:
                self._dht.measure()
            except OSError:
                T.trace(__name__, T.ERROR, 'dht measure error')
                self._dht = None

    ############################################################################
    # @brief    publish tempeature and humidity
    # @return   none
    ############################################################################
    def _publish(self):

        self._state = self._STATE_SLEEP
        T.trace(__name__, T.DEBUG, 'publishing...')
        # get a measurement set, either the real measured  or default 0
        if self._dht != None:
            self._temperature = self._dht.temperature() * self._TEMPERATURE_CORR_FACTOR
            self._humidity = self._dht.humidity() * self._HUMIDITY_CORR_FACTOR
        else:
            self._temperature = 0.0
            self._humidity = 0.0

        self._deactivate_chip()

        T.trace(__name__, T.DEBUG, 'temperature: ' + str(self._temperature))
        T.trace(__name__, T.DEBUG, 'humidity: ' + str(self._humidity))
        self._pub_temperature.publish(str(self._temperature))
        self._pub_humitdity.publish(str(self._humidity))

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
        if self._pwr_gpio != None:
            self._pwr_gpio.off()
            self._pwr_gpio = None

################################################################################
# Scripts
T.configure(__name__, T.INFO)

if __name__ == "__main__":
    # execute only if run as a script
    s = DhtSkill('dev01', '0', 4, NO_VALUE)
    s.start_skill()
    time.sleep(2)
    s.execute_skill()
    time.sleep(2)
    s.execute_skill()
    time.sleep(2)
    s.execute_skill()
    s.stop_skill()
