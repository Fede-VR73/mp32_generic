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

################################################################################
# Methods

################################################################################
# @brief    user main method
# @return   none
################################################################################
def do_user_main():
    print('user main ...')

    if True == src.user_boot.repl_mode:
        print('start repl mode...')
        import webrepl
        webrepl.start()
    else:
        print('start user mode...')
        import webrepl
        webrepl.start()
