import paho.mqtt.client as mqtt
import threading
import json


class CSRO_Dlight(threading.Thread):
    def __init__(self, mac, dev_type):
        threading.Thread.__init__(self)
        self.device_type = dev_type
        self.mac = mac
        self.client = mqtt.Client()
        self.dlight_rgb = [0, 0, 0]
        self.dlight_bright = 0

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('csro/'+self.mac+"/" +
                              self.device_type+"/set/#", qos=0)
        device = {
            "~": "csro/" + self.mac + "/" + self.device_type,
            "name": self.mac + "_"+self.device_type+"_0",
            "uniq_id": self.mac + "_"+self.device_type+"_0",
            "cmd_t": "~/set",
            "bri_cmd_t": "~/set/bright",
            "bri_scl": 10,
            "bri_stat_t": "~/state",
            "bri_val_tpl": "{{value_json.state.bright}}",
            "on_cmd_type": "brightness",
            "pl_on": 1,
            "pl_off": 0,
            "rgb_cmd_t": "~/set/rgb",
            "rgb_stat_t": "~/state",
            "rgb_val_tpl": "{{value_json.state.rgb}}",
            "stat_t": "~/state",
            "stat_val_tpl": "{{value_json.state.on}}",
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
        self.client.publish("csro/light/"+self.mac+"_" +
                            self.device_type+"/config", json_message, retain=True)
        self.client.publish("csro/"+self.mac+"/" +
                            self.device_type+"/available", "online", retain=True)
        self.update_status()

    def on_message(self, client, userdata, msg):
        update = False
        if str(msg.topic) == str("csro/" + self.mac + "/" + self.device_type+"/set"):
            if msg.payload.decode('UTF-8') == "0":
                self.dlight_bright = 0
            elif msg.payload.decode('UTF-8') == "1":
                self.dlight_bright = 10
            update = True
        elif str(msg.topic) == str("csro/" + self.mac + "/" + self.device_type+"/set/bright"):
            if int(msg.payload.decode('UTF-8')) >= 0 and int(msg.payload.decode('UTF-8')) <= 10:
                self.dlight_bright = int(msg.payload.decode('UTF-8'))
                update = True
        elif str(msg.topic) == str("csro/" + self.mac + "/" + self.device_type+"/set/rgb"):
            rgb_value_str = msg.payload.decode('UTF-8').split(",")
            self.dlight_rgb[0] = int(rgb_value_str[0])
            self.dlight_rgb[1] = int(rgb_value_str[1])
            self.dlight_rgb[2] = int(rgb_value_str[2])
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
            "state": {
                "on":  1 if(self.dlight_bright > 0) else 0,
                "bright": self.dlight_bright,
                "rgb": str(self.dlight_rgb[0])+","+str(self.dlight_rgb[1])+","+str(self.dlight_rgb[2])
            }
        }
        state_message = json.dumps(state)
        self.client.publish("csro/"+self.mac+"/" +
                            self.device_type+"/state", state_message)
