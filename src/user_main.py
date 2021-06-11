################################################################################
# filename: user_main.py
# date: 23. Sept. 2020
# username: winkste
# name: Stephan Wink
# description: This module is the local project dependent main module. It is
# expected to be called within the standard boot file in the root directory.
################################################################################

################################################################################
# Imports
from src.mqtt.user_mqtt import check_non_blocking_for_msg
from src.mqtt.user_mqtt import start_mqtt_client
from src.mqtt.user_mqtt import stop_mqtt_client
from time import sleep
from src.user_pins import UserPins
from src.utils.param_set import ParamSet
import src.utils.sys_mode as sys_mode
import src.skills.skill_mgr as skill_mgr
import src.utils.trace as T
from machine import reset
################################################################################
# Methods

################################################################################
# @brief    user initialize method
# @return   none
################################################################################
def do_user_initialize():
    T.trace(__name__, T.DEBUG, 'initialize parameter sets...')
    para = ParamSet()

    T.trace(__name__, T.DEBUG, 'connect to mqtt broker...')
    start_mqtt_client(para.get_mqtt_client_id(), para.get_mqtt_broker_ip(),
                        para.get_mqtt_broker_port(), para.get_mqtt_broker_user(),
                        para.get_mqtt_broker_pwd())

    T.trace(__name__, T.DEBUG, 'startup the configured devices...')
    skill_mgr.start_skill_manager(para.get_device_id(), para.get_capability())


################################################################################
# @brief    user cyclic task methods
# @return   none
################################################################################
def do_user_processes():
    check_non_blocking_for_msg()
    skill_mgr.execute_skills()

################################################################################
# @brief    stop user processes
# @return   none
################################################################################
def stop_user_processes():
    skill_mgr.stop_skill_manager()
    stop_mqtt_client()


################################################################################
# @brief    user main method
# @return   none
################################################################################
def do_user_main():

    T.configure(__name__, T.INFO)
    T.trace(__name__, T.INFO, 'user main ...')
    sys_mode.goto_normal_mode()

    if sys_mode.is_normal_mode_active():
        T.trace(__name__, T.DEBUG, 'user mode...')
        do_user_initialize()
        while sys_mode.is_normal_mode_active():
            do_user_processes()
            if sys_mode.short_check_for_repl_via_button_request():
                goto_repl_mode()
        else:
            stop_user_processes()

    if sys_mode.is_reset_mode_active():
        T.trace(__name__, T.DEBUG, 'reset mode...')
        reset()

    if sys_mode.is_repl_mode_active():
        T.trace(__name__, T.DEBUG, 'repl mode...')
