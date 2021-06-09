################################################################################
# filename: clean_sources.py
# date: 03. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module initiales the parameter sets in the file system.
################################################################################

################################################################################
# Imports
import os

################################################################################
# Functions

################################################################################
# @brief    This function is the main function of this script and is executed
#               in main scope or manually called.
# @return   none
################################################################################
def main():
    #force_github_update()
    delete_all()

################################################################################
# @brief    This function changes the .version file to 0.0.0 to force a github
#               OTA update.
# @return   none
################################################################################
def force_github_update():
    f = open('src/.version', 'w')
    f.write('0.0.0')
    f.close()

################################################################################
# @brief    This function deletes the pymakr version file from the device. this
#           will retrigger a complete update by the pymakr plugin.
# @return   none
################################################################################
def force_pymakr_update():
    os.remove('project.pymakr')

################################################################################
# @brief    This function deletes all files except the boot.py and main.py
# @return   none
################################################################################
def delete_all():
    image = os.listdir()

    for i in image:
        if not remove_tree(i):
            os.remove(i)

################################################################################
# @brief    This function removes the existing directory structure
# @ param   directory structure to delete
# @return   true if folder was succesful removed, else false
################################################################################
def remove_tree(directory):
    try:
        for entry in os.ilistdir(directory):
            is_dir = entry[1] == 0x4000
            if is_dir:
                remove_tree(directory + '/' + entry[0])

            else:
                os.remove(directory + '/' + entry[0])
        os.rmdir(directory)
        return True
    except OSError:
        return False

################################################################################
# Classes
    ############################################################################
    # Member Variables
    ############################################################################
    # Member Functions

################################################################################
# Scripts
if __name__ == "__main__":
    main()
