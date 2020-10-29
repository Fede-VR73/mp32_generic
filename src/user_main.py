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
import src.user_boot
from src.mqtt.user_mqtt import check_non_blocking_for_msg
from src.mqtt.user_mqtt import start_mqtt_client
from src.mqtt.user_mqtt import stop_mqtt_client
from time import sleep
from src.user_pins import UserPins
from src.param_set import ParamSet
import src.skills.skill_mgr as skill_mgr
################################################################################
# Methods

################################################################################
# @brief    user initialize method
# @return   none
################################################################################
def do_user_initialize():
    print('initialize parameter sets...')
    para = ParamSet()

    print('connect to mqtt broker...')
    start_mqtt_client(para.get_mqtt_client_id(), para.get_mqtt_broker_ip(),
                        para.get_mqtt_broker_port(), para.get_mqtt_broker_user(),
                        para.get_mqtt_broker_pwd())

    print('startup the configured devices...')
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
    pins = UserPins()
    print('user main ...')

    if True != src.user_boot.repl_mode:
        print('user mode...')
        do_user_initialize()
        #checks the repl pin every task cycle for 100msec
        while 5 > pins.sample_repl_req_low_state(100):
            do_user_processes()
        else:
            stop_user_processes()

    print('repl mode...')
