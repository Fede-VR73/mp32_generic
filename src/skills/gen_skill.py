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
import time
from src.skills.abs_skill import AbstractSkill
from src.mqtt.user_subs import UserSubs
from src.mqtt.user_pubs import UserPubs
from src.app_info import AppInfo
import src.trace as T

################################################################################
# Variables

################################################################################
# Functions

################################################################################
# Classes
################################################################################
# @brief    This is the generic skill, handling generic features and functions
################################################################################
class GenSkill(AbstractSkill):

    ############################################################################
    # Member Attributes
    device_info_request = None
    pub_fw_ident = None
    pub_fw_version = None
    pub_fw_desc = None
    app_info = None
    EXECUTION_PERIOD = 5000
    health_counter = 0
    pub_health_counter = None
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
        self._skill_name = "gen skill"
        self.device_info_request = UserSubs(self, "any/topic/test", dev_id, "std", skill_entity)
        self.device_info_request.subscribe()
        self.pub_fw_ident = UserPubs("gen/fwident", dev_id)
        self.pub_fw_version = UserPubs("gen/fwversion", dev_id)
        self.pub_fw_desc = UserPubs("gen/fwdesc", dev_id)
        self.app_info = AppInfo()
        self.skill_name = "generic skill"
        self.pub_health_counter = UserPubs("health/tic", dev_id)
        self.health_counter = 0

    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        self.pub_fw_ident.publish(self.app_info.get_fw_identifier())
        self.pub_fw_version.publish(self.app_info.get_fw_version())
        self.pub_fw_desc.publish(self.app_info.get_description())

    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
        current_time = time.ticks_ms()
        if abs(time.ticks_diff(current_time, self._last_time)) > self.EXECUTION_PERIOD:
            self._last_time = current_time
            self.health_counter = self.health_counter + 1
            self.pub_health_counter.publish(str(self.health_counter))

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
T.configure(__name__, T.INFO)

if __name__ == "__main__":
    # execute only if run as a script
    dev = GenSkill('dev01', '0')
    dev.start_skill()
    dev.execute_skill()
    time.sleep(1)
    dev.execute_skill()
    #userSubs = dev.get_subscription()
    #userSubs.cb_test()
