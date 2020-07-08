import paho.mqtt.client as mqtt
import threading
import json
import random
import time
from apscheduler.schedulers.background import BackgroundScheduler


class CSRO_AirSystem(threading.Thread):
    def __init__(self, mac, dev_type):
        threading.Thread.__init__(self)
        self.device_type = dev_type
        self.mac = mac
        self.client = mqtt.Client()
        self.ctemp = 21.5
        self.ttemp = 21.5
        self.mode = "off"
        self.fan = "自动"

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('csro/'+self.mac+"/" +
                              self.device_type+"/set/#", qos=0)
        device = {
            "~": "csro/" + self.mac + "/" + self.device_type,
            "name": self.mac + "_"+self.device_type+"_0",
            "uniq_id": self.mac + "_"+self.device_type+"_0",
            "initial": 20.5,
            "pl_on": "on",
            "pl_off": "off",
            "avty_t": "~/available",
            "curr_temp_t": "~/state",
            "curr_temp_tpl": "{{value_json.state.ctemp | round(1)}}",
            "mode_cmd_t": "~/set/mode",
            "mode_stat_t": "~/state",
            "mode_stat_tpl": "{{value_json.state.mode}}",
            "modes": ["off", "cool", "heat", "dry", "fan_only"],
            "temp_cmd_t": "~/set/temp",
            "temp_stat_t": "~/state",
            "temp_stat_tpl": "{{value_json.state.ttemp}}",
            "precision": 0.1,
            "fan_mode_cmd_t": "~/set/fan",
            "fan_mode_stat_t": "~/state",
            "fan_mode_stat_tpl": "{{value_json.state.fan}}",
            "fan_modes": ["自动", "静音", "低风", "中风", "高风"],
            "min_temp": 16,
            "max_temp": 32,
            "temp_step": 0.5,
            "dev": {
                "ids": self.mac + "_"+self.device_type,
                "name": self.mac + "_"+self.device_type,
                "mf": "南京金星宇节能技术有限公司",
                "mdl": self.device_type.upper(),
                "sw": "2020_02_13"
            }
        }
        json_message = json.dumps(device)
        self.client.publish("csro/climate/"+self.mac+"_" +
                            self.device_type + "/config", json_message, retain=True)
        self.client.publish("csro/"+self.mac+"/" +
                            self.device_type+"/available", "online", retain=True)
        self.update_status()

    def on_message(self, client, userdata, msg):
        update = False
        print(msg.topic, msg.payload)
        if str(msg.topic) == str("csro/" + self.mac + "/" + self.device_type+"/set/temp"):
            self.ttemp = float(msg.payload.decode('UTF-8'))
            update = True
        elif str(msg.topic) == str("csro/" + self.mac + "/" + self.device_type+"/set/mode"):
            self.mode = msg.payload.decode('UTF-8')
            update = True
        elif str(msg.topic) == str("csro/" + self.mac + "/" + self.device_type+"/set/fan"):
            self.fan = msg.payload.decode('UTF-8')
            update = True
        else:
            pass
        if update == True:
            self.update_status()

    def change_ctemp(self):
        if self.mode == "cool" or self.mode == "heat" or self.mode == "dry":
            if (self.ttemp > self.ctemp):
                self.ctemp += random.uniform(0.05, 0.2)
                self.update_status()
            elif (self.ttemp < self.ctemp):
                self.ctemp -= random.uniform(0.05, 0.2)
                self.update_status()
        else:
            self.update_status()

    def run(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.change_ctemp, 'interval', seconds=30)
        scheduler.start()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.will_set("csro/"+self.mac+"/" +
                             self.device_type+"/available", "offline")
        self.client.connect('csro.net.cn', 1883, 60)
        self.client.loop_forever()

    def update_status(self):
        state = {
            "state": {
                "ctemp": self.ctemp,
                "ttemp": self.ttemp,
                "mode": self.mode,
                "fan": self.fan
            }
        }
        state_message = json.dumps(state)
        self.client.publish("csro/"+self.mac+"/" +
                            self.device_type+"/state", state_message)
