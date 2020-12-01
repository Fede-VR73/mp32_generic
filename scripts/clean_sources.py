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
    print('--- clean sources script ---')
    remove_tree('src')
    os.mkdir('src')
    f = open('src/.version', 'w')
    f.write('0.0.4')
    f.close()
