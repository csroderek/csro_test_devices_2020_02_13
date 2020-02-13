import paho.mqtt.client as mqtt
import threading
import json


class Virtual_CSRO_Nlight(threading.Thread):
    def __init__(self, mac, dev_type, num):
        threading.Thread.__init__(self)
        self.device_type = dev_type
        self.mac = mac
        self.channels = num
        self.client = mqtt.Client()
        self.nlight_status = [0, 0, 0, 0]
        

    def on_connect(self, client, userdata, flags, rc):
        # self.client.subscribe('csro/'+self.mac+"/" +
        #                       self.device_type+"/set/#", qos=0)
        for i in range(0, self.channels):
            device = {
                "~": "csro/" + self.mac + "/" + self.device_type,
                "name": self.mac + "_"+self.device_type+"_"+str(i),
                "unique_id": self.mac + "_"+self.device_type+"_"+str(i),
                "cmd_t": "~/set/" + str(i),
                "pl_on": 1,
                "pl_off": 0,
                "stat_t": "~/state",
                "stat_val_tpl": "{{value_json.state["+str(i)+"]}}",
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
            self.client.publish("derek/test/", json_message)
            print(json_message)

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect('csro.net.cn', 1883, 60)
        self.client.loop_forever()

    def update_status(self):
        state = {
            "state": self.nlight_status
        }
        json_message = json.dumps(state)
        self.client.publish()


if __name__ == '__main__':
    nlight1 = Virtual_CSRO_Nlight("abababcdcdcd", "nlight_nb_4k4r", 2)
    nlight1.start()
    print("1 started")
    nligh2 = Virtual_CSRO_Nlight("abababcdcdce", "nlight_nb_4k4r", 2)
    nligh2.start()
    print("2 started")
