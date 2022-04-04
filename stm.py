from stmpy import Driver, Machine
from threading import Thread

import paho.mqtt.client as mqtt
import cv2

class Video_Session:
    def on_init(self):
        print("starting...")
    
    def session_option(self):
        #request participation from both users, might need to change this to accepting only one user and not needing both users
        print("check if want to join")
        
    def start_timer(self, t):
        #starts timer
        print("start timer")
    
    def start_session(self):
        #starts the video stream
        print("start video")
    
    def stop_session(self):
        #stops the video stream
        print("stop video")
    
    def request_user(self):
        #ask if user wants to play game, need both parties to accept the game request.
        print("check if user want ot play game")
    
    def display(self):
        #displays the leaderboard on screen
        print("displaying..")
        
    def close_leaderboard(self):
        #close the leaderboard
        print("closing leaderboard")
        
    def start_game(self):
        print("you are playing cool game :O")
        
    def stop_game(self):
        #stops the game
        print("stoping game...")
        
    


# initial transition
t0 = {"source": "initial",
      "target": "idle",
      "effect": "on_init"}

#The session_option function ask the user if it wants to join a session
t1 = {
    "trigger": "detect",
    "source": "idle",
    "target": "motion_detection",
    "effect": "session_option; start_timer('t', 100)",
}

t2 = {
    "trigger": "join",
    "source": "motion_detection",
    "target": "active",
    "effect": "start_session",
}

t3 = {
    "trigger": "decline",
    "source": "motion_detection",
    "target": "idle",
    "effect": ""
}

t4 = {
    "trigger": "t",
    "source": "motion_detection",
    "target": "idle",
    "effect": ""
}

t5 = {
    "trigger": "exit",
    "source": "active",
    "target": "idle",
    "effect": "stop_session",
}

t6 = {
    "trigger": "view",
    "source": "actve",
    "target": "leaderboard",
    "effect": "display",
}

t7 = {
    "trigger": "back_button",
    "source": "leaderboard",
    "target": "active",
    "effect": "close_leaderboard",
}

t8 = {
    "trigger": "play",
    "source": "active",
    "target": "wait",
    "effect": "request_user",
}

t9 = {
    "trigger": "reject",
    "source": "wait",
    "target": "active",
    "effect": "",
}

t10 = {
    "trigger": "accepted",
    "source": "wait",
    "target": "game",
    "effect": "start_game",
}

t11 = {
    "trigger": "stop",
    "source": "game",
    "target": "active",
    "effect": "stop_game",
}

t12 = {
    "trigger": "view",
    "source": "game",
    "target": "leaderboard",
    "effect": "display",
}


class MQTT_client:
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
        
        #self.stm_driver.send("message", "tick_tock")
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


broker, port = "mqtt.item.ntnu.no", 1883

video = Video_Session()
video_chat_machine = Machine(transitions=[t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12], obj=video, name="video_chat")
video.stm = video_chat_machine

driver = Driver()
driver.add_machine(video_chat_machine)

myclient = MQTT_client()
video.mqtt_client = myclient.client
myclient.stm_driver = driver

driver.start()
myclient.start(broker, port)



