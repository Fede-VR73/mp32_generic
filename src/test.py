#from main.ota_updater import OTAUpdater

#o = OTAUpdater('https://github.com/winkste/mp32_generic')
#print(o.github_repo + '/releases/latest')

#rigth: https://api.github.com/repos/winkste/mp32_generic/releases/latest
#wrong: https://api.github.com/repos/winkste/mp32_generic.git/releases/latest


#latest_release = o.http_client.get('https://api.github.com/repos/winkste/mp32_generic/releases/latest')
#version = latest_release.json()['tag_name']

#from umqtt.simple import MQTTClient
#c = MQTTClient("umqtt_client", '192.168.178.45', 1883, 'winkste', 'sw10950')
#c.connect()
#c.publish(b"foo_topic", b"hello")


#client = MQTTClient('52dc166c-2de7-43c1-88ff-f80211c7a8f6', 'test.mosquitto.org')
#client.connect()

#from machine import Pin

#p0 = Pin(0, Pin.IN)
#print(p0.value())

#from src.user_pins import UserPins

#p = UserPins()

#p.led_on()

#print(p.sample_repl_req_low_state(1000, 10))

#p.led_off()
