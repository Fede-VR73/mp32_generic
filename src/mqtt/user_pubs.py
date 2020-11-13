################################################################################
# filename: user_pub.py
# date: 29. Oct. 2020
# username: winkste
# name: Stephan Wink
# description: This module defines a user publication class to encapsulate the
#              publication handling.
#
################################################################################

################################################################################
# Imports

################################################################################
# Variables

################################################################################
# Functions
# Variables
# mqtt publication callback routine
publish_cb = None

################################################################################
# Functions
################################################################################
# @brief    Set the function for mqtt publications
# @param    pubs_cp     the publication function
# @return   none
################################################################################
def set_mqtt_publish_cb(pubs_cb):
    global publish_cb

    publish_cb = pubs_cb

################################################################################
# Classes

################################################################################
# @brief    This class handles the publication object
################################################################################
class UserPubs:

    ############################################################################
    # Member Attributes
    topic = ''
    payload = ''

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    initializes the Publication object
    # @param    topic           topic of message
    # @param    device          mqtt bus defice identificaiton
    # @param    channel         channel to transfer the topic to
    # @param    skill_entity    skill entity number if multiple instances of a
    #                           skill is used in one deviece
    # @return   none
    ############################################################################
    def __init__(self, topic, device, channel = 'std', skill_entity=None):
        if(None == skill_entity):
            self.topic = channel + "/" + device + "/s/" + topic
        else:
            self.topic = channel + "/" + device + "/s/" +skill_entity +"/"+ topic
        self.payload = ''

    ############################################################################
    # @brief    this function publishes the topic specified in the object
    #           initialization
    # @return   none
    ############################################################################
    def publish(self, payload = ''):
        self.payload = payload
        publish_cb(self.topic, self.payload)
        print("published: " + self.topic + " with payload: " + payload)

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    print("--- test script for user_pubs ---")
    test = UserPubs("gen/fwident", "dev01")
    test.publish("this is a test")
