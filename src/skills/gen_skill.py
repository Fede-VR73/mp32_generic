################################################################################
# filename: gen_skill.py
# date: 26. Oct. 2020
# username: winkste
# name: Stephan Wink
# description: This module generates all generic device mqtt operations
#
################################################################################

################################################################################
# Imports
from src.skills.abs_skill import AbstractSkill
from src.mqtt.user_subs import UserSubs

################################################################################
# Variables

################################################################################
# Functions

################################################################################
# Classes
class GenSkill(AbstractSkill):

    ############################################################################
    # Member Attributes
    device_info_request = None
    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the generic skill object
    # @param    dev_id    device identification
    # @param    skill_entity  skill entity if multiple skills are generated
    # @return   none
    ############################################################################
    def __init__(self, dev_id, skill_entity):
        super().__init__(dev_id, skill_entity)
        self.device_info_request = UserSubs(dev_id + "/any/topic/test", self)
        self.device_info_request.subscribe()

    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        super().start_skill()

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
        super().execute_skill()

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

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    dev = GenSkill('dev01', '0')
    dev.start_skill()
    dev.execute_skill()
    #userSubs = dev.get_subscription()
    #userSubs.cb_test()
