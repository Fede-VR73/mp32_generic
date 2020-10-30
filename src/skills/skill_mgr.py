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
################################################################################
# Variables
active_skills = []

################################################################################
# Functions
################################################################################
# @brief    Initializes and starts the skill manager
# @param    id       device id
# @param    cap      capability
# @return   none
################################################################################
def start_skill_manager(id, cap):

    skill = GenSkill(id, "0")
    skill.start_skill()
    active_skills.append(skill)
    print("skill: " + skill.get_skill_name() + " started")
    print("skill manager started...")

################################################################################
# @brief    Executes the configured skill
# @return   none
################################################################################
def stop_skill_manager():

    for obj in active_skills:
        obj.stop_skill()
    print("skill manager stopped...")

################################################################################
# @brief    Executes the skill manager
# @return   none
################################################################################
def execute_skills():

    for obj in active_skills:
        obj.execute_skill()
    print("executes the skills...")

################################################################################
# Classes

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    start_skill_manager("dev01", 0x20)
    execute_skills()
    stop_skill_manager()
