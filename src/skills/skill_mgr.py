################################################################################
# filename: device_mgr.py
# date: 11. Oct. 2020
# username: winkste
# name: Stephan Wink
# description: This module controls all possible device configurations
#
################################################################################

################################################################################
# Imports
from src.skills.abs_skill import AbstractSkill
from src.skills.gen_skill import GenSkill
from src.skills.mija_skill import MijaSkill
from src.skills.dht_skill import DhtSkill
from src.skills.pir_skill import PirSkill
from src.skills.pir_skill import PIR_SKILL_MODE_POLL
from src.skills.temt6000_skill import Temt6000Skill
from src.skills.neopix_skill import NeopixSkill
from src.skills.relay_skill import RelaySkill
from src.skills.switch_skill import SwitchSkill
from src.skills.switch_skill import SWITCH_SKILL_MODE_POLL

from src.utils.pin_cfg import RELAY_OUT_GPIO
from src.utils.pin_cfg import NEO_DATA_GPIO
from src.utils.pin_cfg import DHT22_PWR_GPIO
from src.utils.pin_cfg import DHT22_DAT_GPIO
from src.utils.pin_cfg import PIR_PWR_GPIO
from src.utils.pin_cfg import PIR_DATA_GPIO
from src.utils.pin_cfg import PIR_LED_GPIO
from src.utils.pin_cfg import TEMP_PWR_GPIO
from src.utils.pin_cfg import TEMP_DAT_ADC
from src.utils.pin_cfg import SWITCH_GPIO
from src.utils.pin_cfg import SWITCH_LED_GPIO

import src.utils.trace as T
################################################################################
# Variables

active_skills = []

################################################################################
# Functions

################################################################################
# @brief    Initializes and starts all skills for the multi sensor device
# @param    id       device id
# @param    cap      capability
# @return   none
################################################################################
def _start_multi_sense(id):

    skill = MijaSkill(id, "0", "Badezimmer oben", bytearray([0x58, 0x2d, 0x34, 0x38, 0x64, 0x37]))
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = MijaSkill(id, "1", "Badezimmer unten", bytearray([0x58, 0x2D, 0x34, 0x37, 0x10, 0x86]))
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = MijaSkill(id, "2", "Elternschlafzimmer", bytearray([0x58, 0x2D, 0x34, 0x3b, 0x8c, 0x66]))
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = MijaSkill(id, "3", "Gaestezimmer", bytearray([0x58, 0x2D, 0x34, 0x39, 0x16, 0xa7]))
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = DhtSkill(id, "0", DHT22_DAT_GPIO, DHT22_PWR_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = PirSkill(id, "0", PIR_DATA_GPIO, PIR_PWR_GPIO, PIR_SKILL_MODE_POLL, PIR_LED_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = Temt6000Skill(id, "0", TEMP_DAT_ADC, TEMP_PWR_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = NeopixSkill(id, '0', NEO_DATA_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + ' started')

    skill = RelaySkill(id, "0", RELAY_OUT_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = SwitchSkill(id, "0", SWITCH_GPIO, SWITCH_SKILL_MODE_POLL, SWITCH_LED_GPIO, True)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

################################################################################
# @brief    Initializes and starts the skill manager
# @param    id       device id
# @param    cap      capability
# @return   none
################################################################################
def start_skill_manager(id, cap):

    skill = GenSkill(id, '0')
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + ' started')

    _start_multi_sense(id)

    T.trace(__name__, T.INFO, 'skill manager started...')

################################################################################
# @brief    Executes the configured skill
# @return   none
################################################################################
def stop_skill_manager():

    for obj in active_skills:
        obj.stop_skill()
    T.trace(__name__, T.INFO, "skill manager stopped...")

################################################################################
# @brief    Executes the skill manager
# @return   always True, for future skill return values
################################################################################
def execute_skills():

    for obj in active_skills:
        obj.execute_skill()
    return True

################################################################################
# Classes

################################################################################
# Scripts

T.configure(__name__, T.INFO)

if __name__ == "__main__":
    # execute only if run as a script
    start_skill_manager("dev01", 0x20)
    execute_skills()
    stop_skill_manager()
