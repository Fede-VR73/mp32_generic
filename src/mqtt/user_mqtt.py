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
import src.utils.trace as T


################################################################################
# Variables
# client object singleton
client = None

################################################################################
# Functions

################################################################################
# @brief    Main function to test and demonstrate the mqtt functionality
# @return   none
################################################################################
def main():
    T.trace(__name__, T.INFO, 'mqtt client test script')
    T.trace(__name__, T.INFO, 'connect to broker')
    start_mqtt_client('umqtt_client', '192.168.178.45', 1883, 'winkste', 'sw10950')
    T.trace(__name__, T.INFO, 'send 1st test publications')
    publish('std/dev102/s/test', 'test1')
    publish('std/dev102/s/test', 'test2')
    publish('std/dev102/s/test', 'test3')
    T.trace(__name__, T.INFO, 'soft restart mqtt client')
    restart()
    T.trace(__name__, T.INFO, 'send 2nd test publications')
    publish('std/dev102/s/test', 'test4')
    publish('std/dev102/s/test', 'test5')
    publish('std/dev102/s/test', 'test6')
    T.trace(__name__, T.INFO, 'stop mqtt client')
    stop_mqtt_client()

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
    client.set_callback(subs_callback)
    client.connect()
    set_mqtt_subscribe_cb(subscribe)
    set_mqtt_unsubscribe_cb(unsubscribe)
    set_mqtt_publish_cb(publish)

################################################################################
# @brief    Stops the mqtt client and disconnects from the mqtt broker
# @return   none
################################################################################
def stop_mqtt_client():
    global client

    if client != None:
        client.disconnect()
        client = None

################################################################################
# @brief    using the mqtt client singleton, this function publishes a messsage
# @param    topic   topic identifier of the messsage
# @param    payload   payload of the message
# @return   none
################################################################################
def publish(topic, payload):
    global client

    if client != None:
        byte_topic = topic.encode('utf-8')
        byte_payload = payload.encode('utf-8')
        client.publish(byte_topic, byte_payload)

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
    if client != None:
        client.check_subscriptions(topic_string, data_string)

################################################################################
# @brief    This function subscribes for a topic and registers a callback
#           function to be called when the topic arrives
# @param    user_subs   user subscription
# @return   none
################################################################################
def subscribe(user_subs):
    global client

    if client != None:
        client.subscribe(user_subs)

################################################################################
# @brief    This function unsubscribes for a topic
# @param    user_subs   user subscription
# @return   none
################################################################################
def unsubscribe(user_subs):
    global client

    if client != None:
        client.unsubscribe(user_subs)

################################################################################
# @brief    This function prints all registered subsciptions
# @return   none
################################################################################
def print_all_subscriptions():
    global client

    if client != None:
        client.print_all_subscriptions()

################################################################################
# @brief    This function checks non blocking for an MQTT incoming message
#           and processes it
# @return   True if execution was successful, else False
################################################################################
def check_non_blocking_for_msg():
    global client
    check_result = True

    if client != None:
        check_result = client.mqtt_cyclic_task()
        if check_result == False:
            check_result = restart()
    else:
        check_result = False

    return(check_result)

################################################################################
# @brief    This function restarts the MQTT client
# @return   True if execution was successful, else False
################################################################################
def restart():
    global client

    restart_result = True

    #resque subscriptions from old client
    subs = client.get_subscriptions()
    id   = client.client_id
    ip   = client.broker_ip
    port = client.broker_port
    user = client.broker_user
    pwd  = client.broker_pwd

    # stop the client
    restart_result = restart_result & stop_mqtt_client()

    # start the client
    restart_result = restart_result & start_mqtt_client(id, ip, port, user, pwd)

    #re-subscribe resqued topics
    for obj in subs:
        restart_result = restart_result & subscribe(obj)
    return restart_result


################################################################################
# Classes
################################################################################
# @brief    This class handles the mqtt connection and organizes all
#           registered subscriptions
################################################################################
class UserMqtt:

    ############################################################################
    # Member Attributes
    client_id               = ''
    broker_ip               = ''
    broker_port             = ''
    broker_user             = ''
    broker_pwd              = ''
    subscriptions           = []
    mqtt_client             = None
    subs_cb                 = None
    _DISCONNECTED           = 0
    _CONNECTED              = 1
    _CONNECTION_DISTURBED   = 2

    _connection_status      = _DISCONNECTED

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
        self._connection_status = self._DISCONNECTED

    ############################################################################
    # @brief    Connects the configured client with the mqtt broker
    # @return   None
    ############################################################################
    def connect(self):
        try:
            self.mqtt_client.connect()
            self._connection_status = self._CONNECTED
        except MQTTException:
            T.trace(__name__, T.ERROR, 'MQTTException:UserMqtt:connect')
            self._connection_status = self._CONNECTION_DISTURBED
        except BaseException:
            T.trace(__name__, T.ERROR, 'BaseException:UserMqtt:connect')
            self._connection_status = self._CONNECTION_DISTURBED


    ############################################################################
    # @brief    Disconnects the configured client from the mqtt broker
    # @return   None
    ############################################################################
    def disconnect(self):
        try:
            self.mqtt_client.disconnect()
            self._connection_status = self._DISCONNECTED
        except BaseException:
            T.trace(__name__, T.ERROR, 'BaseException:UserMqtt:disconnect')
            self._connection_status = self._CONNECTION_DISTURBED

    ############################################################################
    # @brief    This function sets the subscription callback function
    # @param    subs_cb subscription callback function
    # @return   None
    ############################################################################
    def set_callback(self, subs_cb):
        self.subs_cb = subs_cb
        self.mqtt_client.set_callback(self.subs_cb)

    ############################################################################
    # @brief    This function publishes a MQTT message if the client is
    #           connected to a broker
    # @param    topic   topic identifier of the messsage
    # @param    payload   payload of the message
    # @return   None
    ############################################################################
    def publish(self, topic, payload):
        if self._connection_status == self._CONNECTED:
            try:
                self.mqtt_client.publish(topic, payload)
            except BaseException:
                T.trace(__name__, T.ERROR, 'BaseException:UserMqtt:publish')
                self._connection_status = self._CONNECTION_DISTURBED

    ############################################################################
    # @brief    This function subscribes for a topic message and registers a
    #           callback function
    # @param    user_subs   user subscription object including the topic and
    #                       callback
    # @return   None
    ############################################################################
    def subscribe(self, user_subs):
        # append each subscription independent of the connection state
        self.subscriptions.append(user_subs)
        if self._connection_status == self._CONNECTED:
            try:
                self.mqtt_client.subscribe(user_subs.topic)
            except MQTTException:
                T.trace(__name__, T.ERROR, 'MQTTException:UserMqtt:subscribe')
                self._connection_status = self._CONNECTION_DISTURBED
            except BaseException:
                T.trace(__name__, T.ERROR, 'BaseException:UserMqtt:subscribe')
                self._connection_status = self._CONNECTION_DISTURBED

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
    # @brief    This function returns all subscriptions to a new list
    # @return   Returns a list of subscriptions
    ############################################################################
    def get_subscriptions(self):
        subscriptions = []

        for obj in self.subscriptions:
            subscriptions.append(obj)

        return subscriptions

    ############################################################################
    # @brief    This function prints all registered subsciptions
    # @return   none
    ############################################################################
    def print_all_subscriptions(self):
        for obj in self.subscriptions:
            T.trace(__name__, T.DEBUG, obj.topic)

    ############################################################################
    # @brief    MQTT cyclic task to check for messages or reconnect the broker
    # @return   true if check was successful, false on any connection exception
    ############################################################################
    def mqtt_cyclic_task(self):
        mqtt_status = True
        if self._connection_status == self._CONNECTED:
            mqtt_status = mqtt_status & self._check_non_blocking_for_msg()
        elif self._connection_status == self._CONNECTION_DISTURBED:
            for i in range(5):
                mqtt_status = mqtt_status & self._reconnect()
                sleep(i)
        # future return value to trigger a restart of the system
        return True

    ############################################################################
    # @brief    Checks non blocking if any incoming subscriptions need to be
    #           processed
    # @return   true if check was successful, false on any connection exception
    ############################################################################
    def _check_non_blocking_for_msg(self):
        try:
            self.mqtt_client.check_msg()
            return True
        except OSError:
            T.trace(__name__, T.ERROR, 'OSException:UserMqtt:check_non_blocking_for_msg')
            self._connection_status = self._CONNECTION_DISTURBED
            return False
        except BaseException:
            T.trace(__name__, T.ERROR, 'BaseException:UserMqtt:check_non_blocking_for_msg')
            self._connection_status = self._CONNECTION_DISTURBED
            return False

    ############################################################################
    # @brief    Tries to reconnect to MQTT broker
    # @return   true if check was successful, false on any connection exception
    ############################################################################
    def _reconnect(self):
        try:
            self.mqtt_client.connect(False)
            T.trace(__name__, T.INFO, 'UserMqtt:_reconnect -> reconnect successful')
            self._connection_status = self._CONNECTED
            return True
        except OSError:
            T.trace(__name__, T.ERROR, 'OSException:UserMqtt:_reconnect')
            self._connection_status = self._CONNECTION_DISTURBED
            return False
        except BaseException:
            T.trace(__name__, T.ERROR, 'BaseException:UserMqtt:_reconnect')
            self._connection_status = self._CONNECTION_DISTURBED
            return False

################################################################################
# Scripts

T.configure(__name__, T.INFO)

if __name__ == "__main__":
    main()
