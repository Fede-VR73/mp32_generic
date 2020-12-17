################################################################################
# filename: pir_skill.py
# date: 23. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module handles the input signal of the PIR movement sensor.
#               In the first implementation it will only support polling of an
#               input pin. In future implementations also reacting on interrupts
#               shall be possible, therefore a mode variable is defined and
#               handed over to the object during construction
#
#   TODO's: Is debouncing needed here to ensure we don't get wrong activations?
#
################################################################################

################################################################################
# Imports
import time
from src.skills.abs_skill import AbstractSkill
from src.mqtt.user_subs import UserSubs
from src.mqtt.user_pubs import UserPubs
import machine
import src.trace as T

################################################################################
# Variables
_NO_VALUE = 0xff

_PAYLOAD_ON = 'ON'
_PAYLOAD_OFF = 'OFF'

PIR_SKILL_MODE_POLL = 0
PIR_SKILL_MODE_ISR = 1

_PIR_STATE_LOW = 0
_PIR_STATE_HIGH = 1
_PIR_STATE_INIT = 0xff

_PIR_STATE_DICT = {
    _PIR_STATE_LOW: _PAYLOAD_OFF,
    _PIR_STATE_HIGH: _PAYLOAD_ON,

}

_PIR_STATE_DICT_INV = {
    _PIR_STATE_LOW: _PIR_STATE_HIGH,
    _PIR_STATE_HIGH: _PIR_STATE_LOW,

}

################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This is the DHT skill, handling DHT sensor data
################################################################################
class PirSkill(AbstractSkill):

    ############################################################################
    # Member Attributes
    _pub_state = None

    _publish_state = True
    _current_state = _PIR_STATE_INIT
    _current_state_payload = _PAYLOAD_OFF

    EXECUTION_PERIOD = 500

    _pir_pin = _NO_VALUE
    _pwr_pin = _NO_VALUE
    _led_pin = _NO_VALUE

    _pir_gpio = None
    _pwr_gpio = None
    _led_gpio = None

    _led_inf = False
    _pir_mode = PIR_SKILL_MODE_POLL

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the pir skill object
    # @param    dev_id         device identification
    # @param    skill_entity   skill entity if multiple skills are generated
    # @param    _pir_pin       pir input pin
    # @param    _pwr_pin       pir power output pin
    # @param    pir_mode       pir detection mode, currently only poll supported
    # @param    led_pin        led pin displaying the pir state
    # @param    led_inv        led inverse state displaying
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity, pir_pin, pwr_pin = _NO_VALUE,
                    pir_mode=PIR_SKILL_MODE_POLL, led_pin=_NO_VALUE,
                    led_inv=False):
        super().__init__(dev_id, skill_entity)
        self._skill_name = "PIR skill"
        self._pub_state = UserPubs("pir/status", dev_id, "std", skill_entity)

        self._pir_pin = pir_pin
        self._led_pin = led_pin
        self._led_inf = led_inv
        self._pwr_pin = pwr_pin

        self._pir_mode = pir_mode

        self._pir_gpio = None
        self._led_gpio = None
        self._pwr_gpio = None

    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        global _NO_VALUE

        if self._pir_pin != _NO_VALUE:
            self._pir_gpio = machine.Pin(self._pir_pin, machine.Pin.IN,
                                            machine.Pin.PULL_UP)
        if self._led_pin != _NO_VALUE:
            self._led_gpio = machine.Pin(self._led_pin, machine.Pin.OUT)
            T.trace(__name__, T.DEBUG, 'led pin configured: ' + str(self._led_pin))

        if self._pwr_pin != _NO_VALUE:
            self._pwr_gpio = machine.Pin(self._pwr_pin, machine.Pin.OUT)
            self._pwr_gpio.on()

    ############################################################################
    # @brief    checks the pir state transition
    # @return   none
    ############################################################################
    def _check_pir_state_transition(self):
        global _PAYLOAD_OFF, _PAYLOAD_ON, _PIR_STATE_DICT, _PIR_STATE_DICT_INV

        if self._pir_gpio != None:
            new_pir_state = self._pir_gpio.value()
            if new_pir_state != self._current_state:
                self._current_state = new_pir_state
                self._current_state_payload = _PIR_STATE_DICT[self._current_state]
                self._publish_state = True
                T.trace(__name__, T.DEBUG, 'state transition detected...')
                T.trace(__name__, T.DEBUG, 'motion state:' + self._current_state_payload)

        if self._led_gpio != None:
            if self._publish_state == True:
                if self._led_inf == False:
                    self._led_gpio.value(self._current_state)
                    T.trace(__name__, T.DEBUG, 'led state:' + str(self._current_state))
                else:
                    self._led_gpio.value(_PIR_STATE_DICT_INV[self._current_state])
                    T.trace(__name__, T.DEBUG, 'led state:' + str(_PIR_STATE_DICT_INV[self._current_state]))

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
        self._check_pir_state_transition()
        if self._publish_state == True:
            self._publish_state = False
            self._pub_state.publish(self._current_state_payload)

    ############################################################################
    # @brief    executes the incoming subscription callback handler
    # @param    topic       topic identifier of the messsage
    # @param    payload     payload of the message
    # @return   none
    ############################################################################
    def execute_subscription(self, topic, data):
        T.trace(__name__, T.ERROR, 'unexpected subscription')
        T.trace(__name__, T.DEBUG, 'topic: ' + topic)
        T.trace(__name__, T.DEBUG, 'data: ' + data)

    ############################################################################
    # @brief    stopps the skill
    # @return   none
    ############################################################################
    def stop_skill(self):
        super().stop_skill()
        self._pir_gpio = None
        self._current_state = _PIR_STATE_LOW
        if self._led_gpio != None:
            if self._led_inf == False:
                self._led_gpio.value(self._current_state)
                T.trace(__name__, T.DEBUG, 'led state:' + str(self._current_state))
            else:
                self._led_gpio.value(_PIR_STATE_DICT_INV[self._current_state])
                T.trace(__name__, T.DEBUG, 'led state:' + str(_PIR_STATE_DICT_INV[self._current_state]))
            self._led_gpio = None
        if self._pwr_gpio != None:
            self._pwr_gpio.off()
            self._pwr_gpio = None

################################################################################
# Scripts
T.configure(__name__, T.INFO)

if __name__ == "__main__":
    # execute only if run as a script
    T.trace(__name__, T.WARNING, 'no main script defined ')
