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
skill = None
################################################################################
# Functions
################################################################################
# @brief    Initializes and starts the skill manager
# @param    id       device id
# @param    cap      capability
# @return   none
################################################################################
def start_skill_manager(id, cap):
    global skill

    skill = GenSkill(id, "0")
    skill.start_skill()
    print("skill manager started...")

################################################################################
# @brief    Executes the configured skill
# @return   none
################################################################################
def stop_skill_manager():
    global skill

    skill.stop_skill
    print("skill manager stopped...")

################################################################################
# @brief    Executes the skill manager
# @return   none
################################################################################
def execute_skills():
    global skill
    
    skill.execute_skill
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
