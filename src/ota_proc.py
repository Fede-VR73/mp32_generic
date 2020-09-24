################################################################################
# filename: ota_proc.py
# date: 18. Sept. 2020
# username: winkste
# name: Stephan Wink
# description: This module does the project specific OTA update processing
################################################################################

################################################################################
# Imports
from src.ota_updater import OTAUpdater

################################################################################
# Functions

################################################################################
# @brief    downloads, installs and updates to a new version available in github
#           Precondition needed: a wifi connection to the internet
#           When the update have been performed, the controller will be
#           restarted
# @return   none
################################################################################
def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/winkste/mp32_generic')
    if True == o.check_for_update():
        o.download_latest_released_version()
        o.install_update()

################################################################################
# Classes

    ############################################################################
    # Member Functions

################################################################################
# Scripting
