################################################################################
# filename: user_mqtt.py
# date: 07. Oct. 2020
# username: winkste
# name: Stephan Wink
# description: This module controls the MQTT client and the subscriptions to it
#
################################################################################

################################################################################
# Imports
from umqtt.simple import MQTTClient
from umqtt.simple import MQTTException
from time import sleep

################################################################################
# Variables
# client object singleton
client = None

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
def start_mqtt_client(id, ip, port, user, pwd):
    global client

    print(id, ip, port, user, pwd)
    client = UserMqtt(id, ip, port, user, pwd)
    try:
        client.set_callback(subs_callback)
        client.connect()
    except AttributeError:
        print('mqtt client allocation failed...')
    except MQTTException:
        print('mqtt connection error...')

################################################################################
# @brief    Stops the mqtt client and disconnects from the mqtt broker
# @return   none
################################################################################
def stop_mqtt_client():
    global client
    try:
        client.disconnect()
        client = None
    except AttributeError:
        print('mqtt client allocation failed...')
    except MQTTException:
        print('mqtt connection error...')

################################################################################
# @brief    using the mqtt client singleton, this function publishes a messsage
# @param    topic   topic identifier of the messsage
# @param    payload   payload of the message
# @return   none
################################################################################
def publish(topic, payload):
    global client

    try:
        client.publish(topic, payload)
    except AttributeError:
        print('mqtt client not allicated...')
    except OSError:
        print('mqtt connection error in publish...')

################################################################################
# @brief    Callback function for incoming subscriptions
# @param    topic   topic identifier of the messsage
# @param    payload   payload of the message
# @return   none
################################################################################
def subs_callback(topic, data):
    print('Topic received:', topic)
    print('Data received:', data)
    client.check_subscriptions(topic, data)

################################################################################
# @brief    This function subscribes for a topic and registers a callback
#           function to be called when the topic arrives
# @param    topic   topic identifier of the messsage
# @param    cb_func callback function when topic arrives
# @return   none
################################################################################
def subscribe(topic, cb_func):
    global client

    try:
        client.subscribe(topic, cb_func)
    except AttributeError:
        print('mqtt client not allicated...')
    except OSError:
        print('mqtt connection error in subscribe...')

################################################################################
# @brief    This function prints all registered subsciptions
# @return   none
################################################################################
def print_all_subscriptions():
    global client
    client.print_all_subscriptions()

################################################################################
# @brief    This function checks non blocking for an MQTT incoming message
#           and processes it
# @return   none
################################################################################
def check_non_blocking_for_msg():
    global client

    try:
        client.check_non_blocking_for_msg()
        return True
    except AttributeError:
        print('mqtt client not allicated...')
        return False
    except OSError:
        print('mqtt connection error in check_non_blocking_for_msg...')
        return False

################################################################################
# @brief    This is a subscription callback test function
# @param    topic   topic identifier of the messsage
# @param    cb_func callback function when topic arrives
# @return   none
################################################################################
def test_function1(topic, data):
    print('--- Test Function 1 ---')
    print('Topic received:', topic)
    print('Data received:', data)

################################################################################
# @brief    This is a subscription callback test function
# @param    topic   topic identifier of the messsage
# @param    cb_func callback function when topic arrives
# @return   none
################################################################################
def test_function2(topic, data):
    print('--- Test Function 2 ---')
    print('Topic received:', topic)
    print('Data received:', data)

################################################################################
# @brief    This is the main test funcion to test all features of this module
# @return   none
################################################################################
def test_main():
    start_mqtt_client('umqtt_client', '192.168.178.45', 1883, 'winkste', 'sw10950')
    publish(b'test_pub', b'test data')
    subscribe(b'test_sub1', test_function1)
    subscribe(b'test_sub2', test_function2)
    subscribe(b'test_sub1', test_function2)
    print_all_subscriptions()

    while check_non_blocking_for_msg():
        # Non-blocking wait for message

        # Then need to sleep to avoid 100% CPU usage (in a real
        # app other useful actions would be performed instead)
        sleep(1)

################################################################################
# Classes
################################################################################
# @brief    This class handles the mqtt connection and organizes all
#           registered subscriptions
################################################################################
class UserMqtt:

    ############################################################################
    # Member Attributes
    client_id = ''
    broker_ip = ''
    broker_port = ''
    broker_user = ''
    broker_pwd = ''
    subscriptions = []
    mqtt_client = None
    subs_cb = None

    ############################################################################
    # Member Functions
    ############################################################################
    # @brief    initializes the mqtt client
    # @param    client_id       client id
    # @param    broker_ip       broker ip address
    # @param    broker_port     broker ip port
    # @param    user_account    broker user identifier
    # @param    user_pwd        broker user password
    # @return   none
    ############################################################################
    def __init__(self, client_id, broker_ip, broker_port, user_account,
                    user_pwd):
        self.client_id = client_id
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.broker_user = user_account
        self.broker_pwd = user_pwd
        self.mqtt_client = MQTTClient(self.client_id, self.broker_ip,
                                        self.broker_port, self.broker_user,
                                        self.broker_pwd)

    ############################################################################
    # @brief    Connects the configured client with the mqtt broker
    # @return   none
    ############################################################################
    def connect(self):
        self.mqtt_client.connect()

    ############################################################################
    # @brief    Disconnects the configured client from the mqtt broker
    # @return   none
    ############################################################################
    def disconnect(self):
        self.mqtt_client.disconnect()

    ############################################################################
    # @brief    This function sets the subscription callback function
    # @param    subs_cb subscription callback function
    # @return   none
    ############################################################################
    def set_callback(self, subs_cb):
        self.subs_cb = subs_cb
        self.mqtt_client.set_callback(self.subs_cb)

    ############################################################################
    # @brief    This function publishes a MQTT message if the client is
    #           connected to a broker
    # @param    topic   topic identifier of the messsage
    # @param    payload   payload of the message
    # @return   none
    ############################################################################
    def publish(self, topic, payload):
        self.mqtt_client.publish(topic, payload)

    ############################################################################
    # @brief    This function subscribes for a topic message and registers a
    #           callback function
    # @param    topic   topic identifier of the messsage
    # @param    cb_func callback function when topic arrives
    # @return   none
    ############################################################################
    def subscribe(self, topic, cb_func):
        self.subscriptions.append(UserSubs(topic, cb_func))
        self.mqtt_client.subscribe(topic)

    ############################################################################
    # @brief    This function subscribes for a topic message and registers a
    #           callback function
    # @param    topic   topic identifier of the messsage
    # @param    cb_func callback function when topic arrives
    # @return   none
    ############################################################################
    def check_subscriptions(self, topic, payload):
        for obj in self.subscriptions:
            if topic == obj.topic:
                obj.cb_func(topic, payload)

    ############################################################################
    # @brief    This function prints all registered subsciptions
    # @return   none
    ############################################################################
    def print_all_subscriptions(self):
        for obj in self.subscriptions:
            print(obj.topic)

    ############################################################################
    # @brief    Checks non blocking if any incoming subscriptions need to be
    #           processed
    # @return   none
    ############################################################################
    def check_non_blocking_for_msg(self):
        self.mqtt_client.check_msg()


class UserSubs:

    ############################################################################
    # Member Attributes
    topic = ''
    cb_func = None

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    initializes the Subscription object
    # @param    topic       topic of message
    # @param    cb_func     callback function to be called if message arrives
    # @return   none
    #############################################################################
    def __init__(self, topic, cb_func):
        self.topic = topic
        self.cb_func = cb_func

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    test_main()
