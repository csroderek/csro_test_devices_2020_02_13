import paho.mqtt.client as mqtt
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import json
import random

class CSRO_Sensors(threading.Thread):
    def __init__(self, mac, dev_type):
        threading.Thread.__init__(self)
        self.device_type = dev_type
        self.mac = mac
        self.client = mqtt.Client()
        self.co2 = 576
        self.hcho = 0.002
        self.list = ["co2", "hcho"]
        self.unit = ["ppm", "ug/m^3"]
        self.round = [0, 4]
        self.scheduler = BackgroundScheduler()

    def on_connect(self, client, userdata, flags, rc):
        for dev_index in range(0, len(self.list)):
            device = {
                "~": "csro/" + self.mac + "/" + self.device_type,
                "name": self.mac + "_"+self.device_type+"_"+self.list[dev_index],
                "uniq_id": self.mac + "_"+self.device_type+"_"+self.list[dev_index],
                "unit_of_meas": self.unit[dev_index],
                "avty_t": "~/available",
                "stat_t": "~/state",
                "val_tpl": "{{value_json.state[" + str(dev_index) + "]"+"|round("+str(self.round[dev_index])+")"+"}}",
                "dev": {
                    "ids": self.mac + "_"+self.device_type,
                    "name": self.mac + "_"+self.device_type,
                    "mf": "南京金星宇节能技术有限公司",
                    "mdl": self.device_type.upper(),
                    "sw": "2020_02_13"
                }
            }
            json_message = json.dumps(device)
            self.client.publish("csro/sensor/"+self.mac+"_"+self.device_type +
                                "_"+self.list[dev_index]+"/config", json_message, retain=True)
        self.client.publish("csro/"+self.mac+"/" +
                            self.device_type+"/available", "online", retain=True)
        self.update_status()

    def on_message(self, client, userdata, msg):
        pass

    def update_status(self):
        state = {
            "state": [random.randint(543, 1654), random.uniform(0.001, 0.100)]
        }
        state_message = json.dumps(state)
        self.client.publish("csro/"+self.mac+"/" +
                            self.device_type+"/state", state_message)

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.will_set("csro/"+self.mac+"/" +
                             self.device_type+"/available", "offline")
        self.client.connect('csro.net.cn', 1883, 60)
        self.scheduler.add_job(
            self.update_status,
            trigger='interval',
            minutes=1
        )
        self.scheduler.start();
        self.client.loop_forever()



