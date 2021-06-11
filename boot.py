################################################################################
# filename: ota_updater.py
# date: 18. Sept. 2020
# username: winkste
# name: Stephan Wink
# description: This module support the OTA firmware update via github repo.
################################################################################

################################################################################
# Imports
from src.user_boot import do_user_boot
import src.utils.trace as T

################################################################################
# Variables
_NAME_ = 'BOOT'
################################################################################
# Functions

################################################################################
# Classes

    ############################################################################
    # Member Functions

################################################################################
# Scripting
T.trace(__name__, T.INFO, 'starting user boot sequence...')
#print('starting user boot...')
do_user_boot()
