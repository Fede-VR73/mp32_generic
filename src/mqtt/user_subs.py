################################################################################
# filename: user_subs.py
# date: 28. Oct. 2020
# username: winkste
# name: Stephan Wink
# description: This module defines a user subscription class which consumes the
# topic the user whants to wait on and an abstract device. It provides a
# callback function if this subsciption arrives.
#
################################################################################

################################################################################
# Imports
from src.skills.abs_skill import AbstractSkill

################################################################################
# Variables

################################################################################
# Functions
# Variables
# mqtt subscription variable
cb_subscribe = None

################################################################################
# Functions
################################################################################
# @brief    Initializes the mqtt client and connects to the mqtt broker
# @param    id       client id
# @param    ip       broker ip address
# @param    port     broker ip port
# @param    user     broker user identifier
# @param    pwd      broker user password
# @return   none
################################################################################
def set_mqtt_subscribe_cb(subs_cb):
    global subscribe_cb

    subscribe_cb = subs_cb

################################################################################
# Classes

################################################################################
# @brief    This class handles the subscription object
################################################################################
class UserSubs:

    ############################################################################
    # Member Attributes
    topic = ''
    last_payload = b''
    abs_skill = None

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    initializes the Subscription object
    # @param    topic       topic of message
    # @param    abs_skill   abstract skill to connect to when an subscribed
    #                       topic arrives
    # @return   none
    ############################################################################
    def __init__(self, topic, abs_skill):
        self.topic = topic
        self.last_payload = b''
        self.abs_skill = abs_skill

    ############################################################################
    # @brief    this function subscribes the topic specified in the object
    #           initialization
    # @return   none
    ############################################################################
    def subscribe(self):
        subscribe_cb(self)
        print("subscribed to: " + self.topic)

    ############################################################################
    # @brief    callback function interface for arrived subscribed topic
    # @param    topic       topic of message
    # @param    abs_device  abstract device to connect to when an subscribed
    #                       topic arrives
    # @return   none
    ############################################################################
    def callback_on_arrived_topic(self, topic, payload):
        self.topic = topic
        self.last_payload = payload
        self.abs_skill.execute_subscription(topic, payload)

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    print("--- test script for user_subs ---")
