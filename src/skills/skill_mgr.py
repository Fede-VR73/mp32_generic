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
import src.trace as T
################################################################################
# Variables

_GPIO_25        = 25
_GPIO_26        = 26
_GPIO_27        = 27
_GPIO_33        = 33
_GPIO_32        = 32
_GPIO_35        = 35
_GPIO_17        = 17
_GPIO_21        = 21
_GPIO_18        = 18
_GPIO_19        = 19
_GPIO_16        = 16
_GPIO_23        = 23
_RELAY_OUT_GPIO = _GPIO_21
_RELAY_LED_GPIO = _GPIO_19
#_NEO_DATA_GPIO  = _GPIO_27
_NEO_DATA_GPIO  = _GPIO_16
_DHT22_PWR_GPIO = _GPIO_26
_DHT22_DAT_GPIO = _GPIO_25
_PIR_PWR_GPIO   = _GPIO_23
_PIR_DATA_GPIO  = _GPIO_17
_PIR_LED_GPIO   = _GPIO_18
_TEMP_PWR_GPIO  = _GPIO_32
_TEMP_DAT_ADC   = _GPIO_35

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

    skill = MijaSkill(id, "0", "Badezimmer unten", bytearray([0x58, 0x2d, 0x34, 0x38, 0x64, 0x37]))
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = MijaSkill(id, "1", "Badezimmer oben", bytearray([0x58, 0x2D, 0x34, 0x37, 0x10, 0x86]))
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = DhtSkill(id, "0", _DHT22_DAT_GPIO, _DHT22_PWR_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = PirSkill(id, "0", _PIR_DATA_GPIO, _PIR_PWR_GPIO, PIR_SKILL_MODE_POLL, _PIR_LED_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = Temt6000Skill(id, "0", _TEMP_DAT_ADC, _TEMP_PWR_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + " started")

    skill = NeopixSkill(id, '0', _NEO_DATA_GPIO)
    skill.start_skill()
    active_skills.append(skill)
    T.trace(__name__, T.INFO, skill.get_skill_name() + ' started')

    skill = RelaySkill(id, "0", _RELAY_OUT_GPIO, _RELAY_LED_GPIO, 0)
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

    #skill = NeopixSkill(id, '0', _NEO_DATA_GPIO)
    #skill.start_skill()
    #active_skills.append(skill)
    #T.trace(__name__, T.INFO, skill.get_skill_name() + ' started')

    #skill = RelaySkill(id, "0", _RELAY_OUT_GPIO, _RELAY_LED_GPIO, 0)
    #skill.start_skill()
    #active_skills.append(skill)
    #T.trace(__name__, T.INFO, skill.get_skill_name() + " started")


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
# @return   none
################################################################################
def execute_skills():

    for obj in active_skills:
        obj.execute_skill()

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
