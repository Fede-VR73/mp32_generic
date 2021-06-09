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
import src.sys_mode as sys_mode
import network as net

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
    _device_info_request = None
    _pub_fw_ident = None
    _pub_fw_version = None
    _pub_fw_desc = None
    _pub_device_ip = None
    _pub_info_request_pending = False
    _gen_cmd_request = None

    _app_info = None

    _EXECUTION_PERIOD = 5000

    _health_counter = 0
    _pub_health_counter = None

    _CMD_RESET_REQUEST  = 'reset'
    _CMD_REPL_REQUEST   = 'repl'
    _CMD_FW_UPDATE      = 'update'

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
        self._device_info_request = UserSubs(self, "gen/info", dev_id)
        self._gen_cmd_request = UserSubs(self, "gen/cmd", dev_id)
        self._pub_fw_ident = UserPubs("gen/fwident", dev_id)
        self._pub_fw_version = UserPubs("gen/fwversion", dev_id)
        self._pub_fw_desc = UserPubs("gen/desc", dev_id)
        self._pub_device_ip = UserPubs("gen/ip", dev_id)
        self._app_info = AppInfo()
        self.skill_name = "generic skill"
        self._pub_health_counter = UserPubs("health/tic", dev_id)
        self._health_counter = 0
        self._pub_info_request_pending = True

    ############################################################################
    # @brief    starts the skill
    # @return   none
    ############################################################################
    def start_skill(self):
        self._device_info_request.subscribe()
        self._gen_cmd_request.subscribe()


    ############################################################################
    # @brief    executes the skill cyclic task
    # @return   none
    ############################################################################
    def execute_skill(self):
        current_time = time.ticks_ms()
        if abs(time.ticks_diff(current_time, self._last_time)) > self._EXECUTION_PERIOD:
            self._last_time = current_time
            self._health_counter = self._health_counter + 1
            self._pub_health_counter.publish(str(self._health_counter))
        if self._pub_info_request_pending:
            self._publish_gen_info()
            self._pub_info_request_pending = False

    ############################################################################
    # @brief    executes the incoming subscription callback handler
    # @param    topic       topic identifier of the messsage
    # @param    payload     payload of the message
    # @return   none
    ############################################################################
    def execute_subscription(self, topic, data):
        if self._device_info_request.compare_topic(topic):
            T.trace(__name__, T.DEBUG, 'generic information request received')
            #handle publication in main loop, don't public in subscription ISR
            #handler
            self._pub_info_request_pending = True
        elif self._gen_cmd_request.compare_topic(topic):
            T.trace(__name__, T.DEBUG, 'generic command request received')
            T.trace(__name__, T.DEBUG, 'data: ' + data)
            if data == self._CMD_RESET_REQUEST:
                sys_mode.goto_reset_mode()
            elif data == self._CMD_REPL_REQUEST:
                sys_mode.goto_repl_mode()
            elif data == self._CMD_FW_UPDATE:
                sys_mode.goto_reset_mode()
            else:
                T.trace(__name__, T.ERROR, 'unexpected data in subscription')
                T.trace(__name__, T.DEBUG, 'topic: ' + topic)
                T.trace(__name__, T.DEBUG, 'data: ' + data)

        else:
            T.trace(__name__, T.ERROR, 'unexpected subscription')
            T.trace(__name__, T.DEBUG, 'topic: ' + topic)
            T.trace(__name__, T.DEBUG, 'data: ' + data)

    ############################################################################
    # @brief    stopps the skill
    # @return   none
    ############################################################################
    def stop_skill(self):
        self._device_info_request.unsubscribe()
        super().stop_skill()

    ############################################################################
    # @brief    publish generic information on the device
    # @return   none
    ############################################################################
    def _publish_gen_info(self):
        self._pub_fw_ident.publish(self._app_info.get_fw_identifier())
        self._pub_fw_version.publish(self._app_info.get_fw_version())
        self._pub_fw_desc.publish(self._app_info.get_description())
        sta_if = net.WLAN(net.STA_IF)
        ip_cfg = sta_if.ifconfig()
        self._pub_device_ip.publish(ip_cfg[0])

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
