################################################################################
# filename: relay_skill.py
# date: 23. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module generates the single wire relay skill. If a relay
#               PCBA with multiple relays is used, this has to be reflected with
#               several instances of the single relay skill.
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
from micropython import const

################################################################################
# Variables
_NO_VALUE = 0xff

_PAYLOAD_ON = 'ON'
_PAYLOAD_OFF = 'OFF'

################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This is the DHT skill, handling DHT sensor data
################################################################################
class RelaySkill(AbstractSkill):

    ############################################################################
    # Member Attributes
    _pub_state = None
    _sub_toggle = None
    _sub_switch = None

    _publish_state = True
    _current_state_payload = _PAYLOAD_OFF

    EXECUTION_PERIOD = 1000

    _relay_pin = _NO_VALUE
    _led_pin = _NO_VALUE

    _relay_gpio = None
    _led_gpio = None

    _led_inf = False

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the relay skill object
    # @param    dev_id          device identification
    # @param    skill_entity    skill entity if multiple skills are generated
    # @param    relay_pin       relay output pin
    # @param    led_pin         led pin displaying the relay state
    # @param    led_inv         led inverse state displaying
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity, relay_pin, led_pin=_NO_VALUE, led_inv=False):
        super().__init__(dev_id, skill_entity)
        self._skill_name = "Relay skill"
        self._pub_state = UserPubs("relay/state", dev_id, "std", skill_entity)
        self._sub_switch = UserSubs(self, "relay/switch", dev_id, "std", skill_entity)
        self._sub_toggle = UserSubs(self, "relay/toggle", dev_id, "std", skill_entity)

        self._relay_pin = relay_pin
        self._led_pin = led_pin
        self._led_inf = led_inv

        self._relay_gpio = None
        self._led_gpio = None

    ############################################################################
    # @brief    turns the relay off
    # @return   none
    ############################################################################
    def _turn_relay_off(self):
        global _PAYLOAD_OFF
        if self._relay_gpio != None:
            self._relay_gpio.off()
            self._current_state_payload = _PAYLOAD_OFF
            self._publish_state = True

        if self._led_gpio != None:
            if self._led_inf == False:
                self._led_gpio.off()
            else:
                self._led_gpio.on()

    ############################################################################
    # @brief    turns the relay on
    # @return   none
    ############################################################################
    def _turn_relay_on(self):
        global _PAYLOAD_ON
        if self._relay_gpio != None:
            self._relay_gpio.on()
            self._current_state_payload = _PAYLOAD_ON
            self._publish_state = True

        if self._led_gpio != None:
            if self._led_inf == False:
                self._led_gpio.on()
            else:
                self._led_gpio.off()

    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        global _NO_VALUE
        if self._relay_pin != _NO_VALUE:
            self._relay_gpio = machine.Pin(self._relay_pin, machine.Pin.OUT)
        if self._led_pin != _NO_VALUE:
            self._led_gpio = machine.Pin(self._led_pin, machine.Pin.OUT)
        self._turn_relay_off()

        self._sub_switch.subscribe()
        self._sub_toggle.subscribe()

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
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
        global _PAYLOAD_ON, _PAYLOAD_OFF
        if self._sub_toggle.compare_topic(topic):
            T.trace(__name__, T.DEBUG, 'toggle relay received')
            if(self._relay_gpio != None):
                if self._relay_gpio.value() == 0:
                    self._turn_relay_on()
                else:
                    self._turn_relay_off()

        elif self._sub_switch.compare_topic(topic):
            T.trace(__name__, T.DEBUG, 'switch relay received')
            if data == _PAYLOAD_ON:
                self._turn_relay_on()
            elif data == _PAYLOAD_OFF:
                self._turn_relay_off()
            else:
                T.trace(__name__, T.DEBUG, 'switch unexpected payload received')

        else:
            T.trace(__name__, T.ERROR, 'unexpected subscription')
            T.trace(__name__, T.DEBUG, 'topic: ' + topic)
            T.trace(__name__, T.DEBUG, 'data: ' + data)

    ############################################################################
    # @brief    stopps the skill
    # @return   none
    ############################################################################
    def stop_skill(self):
        super().stop_skill()

        self._sub_switch.subscribe()
        self._sub_toggle.subscribe()

        self._turn_relay_off()

        self._relay_gpio = None
        self._led_gpio = None

################################################################################
# Scripts
T.configure(__name__, T.DEBUG)

if __name__ == "__main__":
    pass
    # execute only if run as a script
