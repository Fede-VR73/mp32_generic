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
import src.utils.trace as T

################################################################################
# Variables

################################################################################
# Functions
# Variables
# mqtt subscription variable
subscribe_cb = None
unsubscribe_cb = None

################################################################################
# Functions
################################################################################
# @brief    Set the callback function for mqtt subscription handing
# @param    subs_cb     callback function for the general subscription handling
# @return   none
################################################################################
def set_mqtt_subscribe_cb(subs_cb):
    global subscribe_cb

    subscribe_cb = subs_cb

################################################################################
# @brief    Set Unsubscribe topic function
# @param    unsubs_cb    callback function for unsubscribing the messages
# @return   none
################################################################################
def set_mqtt_unsubscribe_cb(unsubs_cb):
    global unsubscribe_cb

    unsubscribe_cb = unsubs_cb

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
    # @brief    initializes the Publication object
    # @param    abs_skill       abstract skill to connect to when an subscribed
    #                           topic arrives
    # @param    topic           topic of message
    # @param    device          mqtt bus defice identificaiton
    # @param    channel         channel to transfer the topic to
    # @param    skill_entity    skill entity number if multiple instances of a
    #                           skill is used in one deviece
    # @return   none
    ############################################################################
    def __init__(self, abs_skill, topic, device, channel = 'std', skill_entity=None):
        if(None == skill_entity):
            self.topic = channel + "/" + device + "/r/" + topic
        else:
            self.topic = channel + "/" + device + "/r/" +skill_entity +"/"+ topic
        self.last_payload = b''
        self.abs_skill = abs_skill

    ############################################################################
    # @brief    this function subscribes the topic specified in the object
    #           initialization
    # @return   none
    ############################################################################
    def subscribe(self):
        subscribe_cb(self)
        T.trace(__name__, T.INFO, "subscribed to: " + self.topic)

    ############################################################################
    # @brief    this function unsubscribes the topic specified in the object
    #           initialization
    # @return   none
    ############################################################################
    def unsubscribe(self):
        unsubscribe_cb(self)
        T.trace(__name__, T.INFO, "unsubscribed to: " + self.topic)

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

    ############################################################################
    # @brief    compares a given topic with the initialized topic
    # @param    topic       topic of message
    # @return   True if equal, else false
    ############################################################################
    def compare_topic(self, topic):
        return self.topic == topic

################################################################################
# Scripts
T.configure(__name__, T.INFO)

if __name__ == "__main__":
    # execute only if run as a script
    print("--- test script for user_subs ---")
