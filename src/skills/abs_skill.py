################################################################################
# filename: abs_skill.py
# date: 28. Oct. 2020
# username: winkste
# name: Stephan Wink
# description: This module generates a definition of the super class for skills
#
################################################################################

################################################################################
# Imports
import time

################################################################################
# Variables

################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This class defines the abstract skill blueprint. All following
#           will derive from this to have a common interface.
################################################################################
class AbstractSkill:

    ############################################################################
    # Member Attributes
    _skill_name = "abstract skill"
    _last_time = 0
    _dev_id = 'dev00'
    _skill_entity = '0'

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the AbstractSkill object
    # @param    dev_id          device name
    # @param    skill_entity    skill entity if multiple skills are generated
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity = '0'):
        self._dev_id = dev_id
        self._skill_entity = skill_entity
        self._last_time = time.ticks_ms()

    ############################################################################
    # @brief    Getter function for the skill name
    # @return   none
    ############################################################################
    def get_skill_name(self):
        return self._skill_name

    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        print("device " + self._skill_name + " started...")

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
        print("execute " + self._skill_name)

    ############################################################################
    # @brief    executes the incoming subscription callback handler
    # @param    topic       topic identifier of the messsage
    # @param    payload     payload of the message
    # @return   none
    ############################################################################
    def execute_subscription(self, topic, payload):
        print("subscription " + topic + " for device: " + self._dev_id + " received")
        print("payload: " + payload)
    ############################################################################
    # @brief    stopps the skill
    # @return   none
    ############################################################################
    def stop_skill(self):
        print("stop " + self._skill_name)

################################################################################
# Scripts
