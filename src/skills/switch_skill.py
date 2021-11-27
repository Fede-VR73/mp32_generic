################################################################################
# filename: switch_skill.py
# date: 07. Apr. 2021
# username: winkste
# name: Stephan Wink
# description: This module handles the input signal of a switch.
#               In the first implementation it will only support polling of an
#               input pin. In future implementations also reacting on interrupts
#               shall be possible, therefore a mode variable is defined and
#               handed over to the object during construction
#
#
#
################################################################################

################################################################################
# Imports
import time
from src.skills.abs_skill import AbstractSkill
from src.mqtt.user_subs import UserSubs
from src.mqtt.user_pubs import UserPubs
import machine
import src.utils.trace as T

################################################################################
# Variables
_NO_VALUE = 0xff
_SWITCH_OFF_TIME = 1000

SWITCH_SKILL_MODE_POLL = 0
SWITCH_SKILL_MODE_ISR = 1

_SWITCH_STATE_LOW = 0
_SWITCH_STATE_HIGH = 1
_SWITCH_STATE_INIT = 0xff

_SWITCH_STATE_DICT_INV = {
    _SWITCH_STATE_LOW: _SWITCH_STATE_HIGH,
    _SWITCH_STATE_HIGH: _SWITCH_STATE_LOW,

}

_RESTART_TRIGGER_THRESHOLD = 5
_RESTART_TRIGGER_TIMEOUT = 10000


################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This is the switch skill, handling a switch input signal
################################################################################
class SwitchSkill(AbstractSkill):

    ############################################################################
    # Member Attributes
    _pub_state = None

    _publish_state = True
    _current_state = _SWITCH_STATE_INIT

    _switch_pin = _NO_VALUE
    _led_pin = _NO_VALUE

    _switch_gpio = None
    _led_gpio = None

    _led_inf = False
    _swith_mode = SWITCH_SKILL_MODE_POLL

    _switch_trigger = _SWITCH_STATE_HIGH
    _switch_state_published = True

    _restart_trigger_cnt = 0
    _last_trigger_time = 0


    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the switch skill object
    # @param    dev_id         device identification
    # @param    skill_entity   skill entity if multiple skills are generated
    # @param    switch_pin     switch input pin
    # @param    switch_mode    switch detection mode, currently only poll supported
    # @param    led_pin        led pin displaying the switch state
    # @param    led_inv        led inverse state displaying
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity, switch_pin,
                    switch_mode=SWITCH_SKILL_MODE_POLL, led_pin=_NO_VALUE,
                    led_inv=False):
        super().__init__(dev_id, skill_entity)

        self._skill_name    = "SWITCH skill"
        self._pub_state     = UserPubs("switch/triggered", dev_id, "std", skill_entity)

        self._switch_pin    = switch_pin
        self._led_pin       = led_pin
        self._led_inf       = led_inv

        self._switch_mode   = switch_mode

        self._switch_gpio   = None
        self._led_gpio      = None

        self._switch_trigger = _SWITCH_STATE_LOW

        self._restart_trigger_cnt = 0
        self._last_trigger_time = 0


    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        global _NO_VALUE

        if self._switch_pin != _NO_VALUE:
            self._switch_gpio = machine.Pin(self._switch_pin, machine.Pin.IN)
        if self._led_pin != _NO_VALUE:
            self._led_gpio = machine.Pin(self._led_pin, machine.Pin.OUT)
            T.trace(__name__, T.DEBUG, 'led pin configured: ' + str(self._led_pin))

    ############################################################################
    # @brief    checks the switch state transition
    # @return   none
    ############################################################################
    def _check_switch_state_transition(self):

        if self._switch_gpio != None:
            new_switch_state = self._switch_gpio.value()
            if new_switch_state != self._current_state:
                self._current_state = new_switch_state
                T.trace(__name__, T.DEBUG, 'state transition detected...')
                if new_switch_state == self._switch_trigger:
                    self._publish_state = True
                    self._inc_restart_trigger()

        if self._led_gpio != None:
            if self._led_inf == False:
                self._led_gpio.value(self._current_state)
            else:
                self._led_gpio.value(_SWITCH_STATE_DICT_INV[self._current_state])

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):

        current_time = time.ticks_ms()
        # check if we need to switch back 'ON' to 'OFF' state after time X
        if self._switch_state_published:
            if abs(time.ticks_diff(current_time, self._last_time)) > _SWITCH_OFF_TIME:
                self._pub_state.publish('OFF')
                self._switch_state_published = False

        self._check_switch_state_transition()
        if self._publish_state == True:
            self._publish_state = False
            self._pub_state.publish('ON')
            self._last_time = current_time
            self._switch_state_published = True

        self._check_for_restart_request()

    ############################################################################
    # @brief    increment the restart trigger
    # @return   none
    ############################################################################
    def _inc_restart_trigger(self):
        self._restart_trigger_cnt += 1
        self._last_trigger_time = time.ticks_ms()
        T.trace(__name__, T.DEBUG, 'trigger counter:' + str(self._restart_trigger_cnt))

    ############################################################################
    # @brief    checks for a restart request per switch
    # @return   none
    ############################################################################
    def _check_for_restart_request(self):
        if self._restart_trigger_cnt > _RESTART_TRIGGER_THRESHOLD:
            self._restart_trigger_cnt = 0
            T.trace(__name__, T.INFO, 'restart triggered')
            import machine
            machine.reset()
        else:
            current_time = time.ticks_ms()
            if abs(time.ticks_diff(current_time, self._last_trigger_time)) > _RESTART_TRIGGER_TIMEOUT:
                self._restart_trigger_cnt = 0





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
        self._switch_gpio = None
        self._current_state = _SWITCH_STATE_LOW
        if self._led_gpio != None:
            if self._led_inf == False:
                self._led_gpio.value(self._current_state)
                T.trace(__name__, T.DEBUG, 'led state:' + str(self._current_state))
            else:
                self._led_gpio.value(_SWITCH_STATE_DICT_INV[self._current_state])
                T.trace(__name__, T.DEBUG, 'led state:' + str(_SWITCH_STATE_DICT_INV[self._current_state]))
            self._led_gpio = None

################################################################################
# Scripts
T.configure(__name__, T.INFO)

if __name__ == "__main__":
    # execute only if run as a script
    T.trace(__name__, T.WARNING, 'no main script defined ')
