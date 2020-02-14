import paho.mqtt.client as mqtt
import threading
import json


class CSRO_Motor(threading.Thread):
    def __init__(self, mac, dev_type, num):
        threading.Thread.__init__(self)
        self.device_type = dev_type
        self.mac = mac
        self.channels = num
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('csro/'+self.mac+"/" +
                              self.device_type+"/set/#", qos=0)
        for dev_index in range(0, self.channels):
            device = {
                "~": "csro/" + self.mac + "/" + self.device_type,
                "name": self.mac + "_"+self.device_type+"_"+str(dev_index),
                "uniq_id": self.mac + "_"+self.device_type+"_"+str(dev_index),
                "cmd_t": "~/set/" + str(dev_index),
                "pos_t": "~/state",
                "val_tpl": "{{value_json.state["+str(dev_index)+"]}}",
                "pl_open": "open",
                "pl_stop": "stop",
                "pl_cls": "close",
                "dev_cla": "curtain",
                "avty_t": "~/available",
                "dev": {
                    "ids": self.mac + "_"+self.device_type,
                    "name": self.mac + "_"+self.device_type,
                    "mf": "南京金星宇节能技术有限公司",
                    "mdl": self.device_type.upper(),
                    "sw": "2020_02_13"
                }
            }
            json_message = json.dumps(device)
            self.client.publish("csro/cover/"+self.mac+"_"+self.device_type +
                                "_"+str(dev_index)+"/config", json_message)
        self.client.publish("csro/"+self.mac+"/" +
                            self.device_type+"/available", "online")
        self.update_status()

    def on_message(self, client, userdata, msg):
        print(msg.topic, msg.payload)
        update = False
        for dev_index in range(0, self.channels):
            if str(msg.topic) == str("csro/" + self.mac + "/" + self.device_type+"/set/"+str(dev_index)):
                update = True
            else:
                pass
        if update == True:
            self.update_status()

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.will_set("csro/"+self.mac+"/" +
                             self.device_type+"/available", "offline")
        self.client.connect('csro.net.cn', 1883, 60)
        self.client.loop_forever()

    def update_status(self):
        state = {
            "state": [50, 50]
        }
        state_message = json.dumps(state)
        self.client.publish("csro/"+self.mac+"/" +
                            self.device_type+"/state", state_message)
