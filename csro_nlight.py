import paho.mqtt.client as mqtt
import threading


class Virtual_CSRO_Nlight(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)
        self.channels = n
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('csro/#', qos=0)
        print("Connected with result code: " + str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect('csro.net.cn', 1883, 60)
        self.client.loop_forever()


if __name__ == '__main__':

    nlight1 = Virtual_CSRO_Nlight(1)
    nlight1.start()
    print("1 started")
    nligh2 = Virtual_CSRO_Nlight(2)
    nligh2.start()
    print("2 started")
