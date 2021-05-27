################################################################################
# filename: log_dump.py
# date: 01 May 2021
# username: winkste
# name: Stephan Wink
# description: This module dumps the trace log file and prints all messages
#               to the console. After printing, the logfile will be erased.
################################################################################

################################################################################
# Imports
import os

################################################################################
# Global Variables

################################################################################
# Functions

################################################################################
# @brief    Main function of script
# @return   none
################################################################################
def main():
    print('--- log file dump script ---')
    print('retrieving file size...')
    print_log_file_size()
    print('dumping file...')
    dump_log_file()
    print('deleting file...')
    delete_log_file()


################################################################################
# @brief    Print log file file size
# @return   none
################################################################################
def print_log_file_size():
    try:
        file_stat = os.stat('.logs')
        print('File size in bytes is: ', file_stat[6])

    except OSError:
        #file not found, try to log
        print('File not found.')

################################################################################
# @brief    Dump the log file data and print to console
# @return   none
################################################################################
def dump_log_file():
    try:
        file = open('.logs')
        logs = file.readline()
        while logs != '':
            print(logs, end='')
            logs = file.readline()
        print('File dump completed.')
        file.close()
    except OSError:
        print('File not found.')


################################################################################
# @brief    Delete log file
# @return   none
################################################################################
def delete_log_file():
    try:
        file_stat = os.remove('.logs')
        print('Log file removed.')

    except OSError:
        #file not found, try to log
        print('File not found.')

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
