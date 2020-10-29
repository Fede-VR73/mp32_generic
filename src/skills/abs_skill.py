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

################################################################################
# Variables

################################################################################
# Functions

################################################################################
# Classes
class AbstractSkill:

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the AbstractSkill object
    # @param    dev_id          device name
    # @param    skill_entity    skill entity if multiple skills are generated
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity = '0'):
        self.dev_id = dev_id
        self.skill_entity = skill_entity

    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        print("device " + self.dev_id + " started...")

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
        print("execute " + self.dev_id)

    ############################################################################
    # @brief    executes the incoming subscription callback handler
    # @param    topic       topic identifier of the messsage
    # @param    payload     payload of the message
    # @return   none
    ############################################################################
    def execute_subscription(self, topic, payload):
        print("subscription " + topic + " for device: " + self.dev_id + " received")

    ############################################################################
    # @brief    stopps the skill
    # @return   none
    ############################################################################
    def stop_skill(self):
        print("stop " + self.dev_id)

################################################################################
# Scripts
