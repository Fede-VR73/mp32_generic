################################################################################
# filename: neopix_skill.py
# date: 26. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module controls a single neo pixel RGB led.
#
################################################################################

################################################################################
# Imports
import time
from src.skills.abs_skill import AbstractSkill
from src.mqtt.user_subs import UserSubs
from src.mqtt.user_pubs import UserPubs
import machine, neopixel
import src.trace as T
from micropython import const

################################################################################
# Variables

_ON             = 1
_OFF            = 0
_TOGGLE         = 2

_PAYLOAD_ON     = 'ON'
_PAYLOAD_OFF    = 'OFF'



################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This is the DHT skill, handling DHT sensor data
################################################################################
class NeopixSkill(AbstractSkill):

    ############################################################################
    # Member Attributes
    NO_VALUE       = 0xff

    _pub_state = None
    _pub_color = None
    _pub_bright = None

    _sub_toggle = None
    _sub_switch = None
    _sub_color = None
    _sub_bright = None

    _publish_state = True
    _current_state_payload = _PAYLOAD_OFF
    _color = [255, 0, 0]
    _brightness = 100
    _current_state = _OFF
    _neo_cmd = NO_VALUE

    EXECUTION_PERIOD = 1000

    _neo_pin = NO_VALUE
    _neo_gpio = None


    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the neo pixel skill object
    # @param    dev_id          device identification
    # @param    skill_entity    skill entity if multiple skills are generated
    # @param    neo_pin         relay output pin
    # @param    led_pin         led pin displaying the relay state
    # @param    led_inv         led inverse state displaying
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity, neo_pin):
        super().__init__(dev_id, skill_entity)
        self._skill_name = "NeoPixel skill"
        self._pub_state = UserPubs("neo_one/state", dev_id, "std", skill_entity)
        self._pub_color = UserPubs("neo_one/color", dev_id, "std", skill_entity)
        self._pub_bright = UserPubs("neo_one/brightness", dev_id, "std", skill_entity)

        self._sub_switch = UserSubs(self, "neo_one/switch", dev_id, "std", skill_entity)
        self._sub_toggle = UserSubs(self, "neo_one/toggle", dev_id, "std", skill_entity)
        self._sub_color = UserSubs(self, "neo_one/color", dev_id, "std", skill_entity)
        self._sub_bright = UserSubs(self, "neo_one/brightness", dev_id, "std", skill_entity)

        self._neo_pin = neo_pin

        self._neo_gpio = None

    ############################################################################
    # @brief    turns the neo pixels element off
    # @return   none
    ############################################################################
    def _turn_neo_off(self):
        global _PAYLOAD_OFF, _OFF
        if self._neo_gpio != None:
            self._neo_gpio[0] = tuple([0, 0, 0])
            self._neo_gpio.write()
            self._current_state_payload = _PAYLOAD_OFF
            self._current_state = _OFF

    ############################################################################
    # @brief    turns the neo pixels element on with the given color and
    #           brightness
    # @return   none
    ############################################################################
    def _turn_neo_on(self):
        global _PAYLOAD_ON, _ON
        if self._neo_gpio != None:
            self._neo_gpio[0] = tuple(self._color)
            self._neo_gpio.write()
            self._current_state_payload = _PAYLOAD_ON
            self._current_state = _ON

    ############################################################################
    # @brief    executes neo command
    # @return   none
    ############################################################################
    def _execute_neo_cmd(self):
        global _ON, _OFF, _TOGGLE
        if self._neo_cmd == _ON:
            self._turn_neo_on()
            self._publish_state = True
        elif self._neo_cmd == _OFF:
            self._turn_neo_off()
            self._publish_state = True
        elif self._neo_cmd == _TOGGLE:
            if self._current_state == _OFF:
                self._turn_neo_on()
            else:
                self._turn_neo_off()
            self._publish_state = True
        self._neo_cmd = self.NO_VALUE


    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        if self._neo_pin != self.NO_VALUE:
            self._neo_gpio = neopixel.NeoPixel(machine.Pin(self._neo_pin), 1)
        self._turn_neo_off()
        self._sub_switch.subscribe()
        self._sub_toggle.subscribe()
        self._sub_color.subscribe()
        self._sub_bright.subscribe()

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):

        self._execute_neo_cmd()

        if self._publish_state == True:
            self._publish_state = False
            self._pub_state.publish(self._current_state_payload)
            self._pub_bright.publish(str(self._brightness))
            color = str(self._color[0]) + ', ' + str(self._color[1]) + ', ' \
                        + str(self._color[2])
            self._pub_color.publish(color)

    ############################################################################
    # @brief    executes the incoming subscription callback handler
    # @param    topic       topic identifier of the messsage
    # @param    payload     payload of the message
    # @return   none
    ############################################################################
    def execute_subscription(self, topic, data):
        global _PAYLOAD_ON, _PAYLOAD_OFF, _TOGGLE, _ON, _OFF
        if self._sub_toggle.compare_topic(topic):
            T.trace(__name__, T.DEBUG, 'toggle neo received')
            self._neo_cmd = _TOGGLE

        elif self._sub_switch.compare_topic(topic):
            T.trace(__name__, T.DEBUG, 'switch neo received')
            if data == _PAYLOAD_ON:
                self._neo_cmd = _ON
            elif data == _PAYLOAD_OFF:
                self._neo_cmd = _OFF
            else:
                T.trace(__name__, T.ERROR, 'switch unexpected payload received')

        elif self._sub_bright.compare_topic(topic):
            self._brightness = int(data)
            if self._brightness != 0:
                self._neo_cmd = _ON
            else:
                self._neo_cmd = _OFF

        elif self._sub_color.compare_topic(topic):

            # conversion from string to integer list
            a = [int(s) for s in data.split(',') if s.isdigit()]
            # validation of data: 1. initial length, 2. range check
            if len(a) == 3:
                b = [s for s in a if s <= 255 and s >= 0]
                # only if all 3 elements of the RGB are in range, the size of
                # the list stays at 3
                if len(b) == 3:
                    self._color = b
                    self._neo_cmd = _ON
                else:
                    T.trace(__name__, T.WARNING, 'data out of range')
                    T.trace(__name__, T.WARNING, 'topic: ' + topic)
                    T.trace(__name__, T.WARNING, 'data: ' + data)

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

        self._turn_neo_off()

        self._neo_gpio = None

################################################################################
# Scripts
T.configure(__name__, T.DEBUG)

if __name__ == "__main__":
    pass
    # execute only if run as a script
