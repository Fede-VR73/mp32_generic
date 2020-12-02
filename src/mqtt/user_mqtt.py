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
from src.mqtt.user_subs import UserSubs
from src.mqtt.user_subs import set_mqtt_subscribe_cb
from src.mqtt.user_subs import set_mqtt_unsubscribe_cb
from src.mqtt.user_pubs import UserPubs
from src.mqtt.user_pubs import set_mqtt_publish_cb
import src.trace as T

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

    client = UserMqtt(id, ip, port, user, pwd)
    try:
        client.set_callback(subs_callback)
        client.connect()
        set_mqtt_subscribe_cb(subscribe)
        set_mqtt_unsubscribe_cb(unsubscribe)
        set_mqtt_publish_cb(publish)
    except AttributeError:
        T.trace(__name__, T.ERROR, 'mqtt client allocation failed...')
    except MQTTException:
        T.trace(__name__, T.ERROR, 'mqtt connection error...')

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
        T.trace(__name__, T.ERROR, 'mqtt client allocation failed...')
    except MQTTException:
        T.trace(__name__, T.ERROR, 'mqtt connection error...')

################################################################################
# @brief    using the mqtt client singleton, this function publishes a messsage
# @param    topic   topic identifier of the messsage
# @param    payload   payload of the message
# @return   none
################################################################################
def publish(topic, payload):
    global client
    byte_topic = topic.encode('utf-8')
    byte_payload = payload.encode('utf-8')

    try:
        client.publish(byte_topic, byte_payload)
    except AttributeError:
        T.trace(__name__, T.ERROR, 'mqtt client not allocated...')
    except OSError:
        T.trace(__name__, T.ERROR, 'mqtt connection error in publish...')

################################################################################
# @brief    Callback function for incoming subscriptions
# @param    topic   topic identifier of the messsage
# @param    payload   payload of the message
# @return   none
################################################################################
def subs_callback(topic, data):
    topic_string = topic.decode('utf-8')
    data_string = data.decode('utf-8')
    T.trace(__name__, T.DEBUG, 'Topic received:' + topic_string)
    T.trace(__name__, T.DEBUG, 'Data received:' + data_string)
    client.check_subscriptions(topic_string, data_string)

################################################################################
# @brief    This function subscribes for a topic and registers a callback
#           function to be called when the topic arrives
# @param    user_subs   user subscription
# @return   none
################################################################################
def subscribe(user_subs):
    global client

    try:
        client.subscribe(user_subs)
    except AttributeError:
        T.trace(__name__, T.ERROR, 'mqtt client not allocated...')
    except OSError:
        T.trace(__name__, T.ERROR, 'mqtt connection error in subscribe...')

################################################################################
# @brief    This function unsubscribes for a topic
# @param    user_subs   user subscription
# @return   none
################################################################################
def unsubscribe(user_subs):
    global client

    try:
        client.unsubscribe(user_subs)
    except AttributeError:
        T.trace(__name__, T.ERROR, 'mqtt client not allocated...')
    except OSError:
        T.trace(__name__, T.ERROR, 'mqtt connection error in unsubscribe...')

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
        T.trace(__name__, T.ERROR, 'mqtt client not allocated...')
        return False
    except OSError:
        T.trace(__name__, T.ERROR, 'mqtt connection error in check_non_blocking_for_msg...')
        return False

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
    # @param    user_subs   user subscription object including the topic and
    #                       callback
    # @return   none
    ############################################################################
    def subscribe(self, user_subs):
        self.subscriptions.append(user_subs)
        self.mqtt_client.subscribe(user_subs.topic)

    ############################################################################
    # @brief    This function unsubscribes for a topic message
    # @param    user_subs   user subscription object including the topic and
    #                       callback
    # @return   none
    ############################################################################
    def unsubscribe(self, user_subs):
        for obj in self.subscriptions:
            if user_subs.topic == obj.topic:
                self.subscriptions.remove(obj)

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
                obj.callback_on_arrived_topic(topic, payload)

    ############################################################################
    # @brief    This function prints all registered subsciptions
    # @return   none
    ############################################################################
    def print_all_subscriptions(self):
        for obj in self.subscriptions:
            T.trace(__name__, T.DEBUG, obj.topic)

    ############################################################################
    # @brief    Checks non blocking if any incoming subscriptions need to be
    #           processed
    # @return   none
    ############################################################################
    def check_non_blocking_for_msg(self):
        self.mqtt_client.check_msg()

################################################################################
# Scripts

T.configure(__name__, T.INFO)

if __name__ == "__main__":
    print("--- user_mqtt test script ---")
