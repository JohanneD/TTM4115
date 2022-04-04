from stmpy import Driver, Machine
from threading import Thread

import paho.mqtt.client as mqtt
import cv2

def enableVideo():
    cam = cv2.VideoCapture(0)

    while True:
        ret, image = cam.read()
        cv2.imshow('test', image)
        k=cv2.waitKey(1)
        if k!= -1:
            break
    
    cv2.imwrite('/home/pi/test.jpg', image)
    cam.release()
    cv2.destroyAllWindows()

class Tick:
    def on_init(self):
        print("Init!")
        self.ticks = 0
        self.tocks = 0

    def send_mqtt_tick(self):
        print("Tick! {}".format(self.ticks))
        self.ticks = self.ticks + 1
        self.mqtt_client.publish("tick", self.ticks)

    def send_mqtt_tock(self):
        print("Tock! {}".format(self.tocks))
        self.tocks = self.tocks + 1
        self.mqtt_client.publish("tock", self.ticks)


# initial transition
t0 = {"source": "initial", "target": "s_tick", "effect": "on_init"}

t1 = {
    "trigger": "message",
    "source": "s_tick",
    "target": "s_tock",
    "effect": "send_mqtt_tick",
}

t2 = {
    "trigger": "message",
    "source": "s_tock",
    "target": "s_tick",
    "effect": "send_mqtt_tock",
}

class MQTT_Client_1:
    def __init__(self):
        self.count = 0
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("on_connect(): {}".format(mqtt.connack_string(rc)))

    def on_message(self, client, userdata, msg):
        if msg.topic == "ttm4115/3/test":
            print(f"on_message(): topic: {msg.topic}:{str(msg.payload)}")
        
        self.stm_driver.send("message", "tick_tock")
        if str(msg.payload.decode("utf-8")) == "startVideo":
            print("testing hi")
            enableVideo()

    def start(self, broker, port):

        print("Connecting to {}:{}".format(broker, port))
        self.client.connect(broker, port)

        self.client.subscribe("ttm4115/3/test")

        try:
            # line below should not have the () after the function!
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()
            
# broker, port = 'iot.eclipse.org', 1883
broker, port = "mqtt.item.ntnu.no", 1883

tick = Tick()
tick_tock_machine = Machine(transitions=[t0, t1, t2], obj=tick, name="tick_tock")
tick.stm = tick_tock_machine

driver = Driver()
driver.add_machine(tick_tock_machine)

myclient = MQTT_Client_1()
tick.mqtt_client = myclient.client
myclient.stm_driver = driver

driver.start()
myclient.start(broker, port)