from stmpy import Driver, Machine
from threading import Thread

import keyboard
import paho.mqtt.client as mqtt
import cv2
import camera_motion as camera
import googleMeet
#from six.moves import input
import time
from pynput.keyboard import Key, Controller

class Video_Session:
    motion = camera.Detector()
    
    def on_init(self):
        print("starting...")
        #motion = motion_detector.Detector()
        
    def get_motion(self):
        return self.motion.stop_motion()
    
    def motion_detection(self):
        print("detecting motion...")
        detect = self.motion
        detect.stop_motion()
        detect.detect_motion()
        if detect:
            #self.session_option()
            #self.start_timer(10)
            self.stm.send('detect')
    
    #both session option and start timer is called when motion is detected.
    def session_option(self):
        #request participation from both users, might need to change this to accepting only one user and not needing both users
        #cam.release()
        #cv2.destroyAllWindows()
        print("do you want to join session? (Y/N): ")
        timer = time.perf_counter()
        while True:
            key = cv2.waitKey(1) & 0xFF
            new_time = time.perf_counter()
            timediff = new_time - timer
            if key == ord("y"):
                myclient.send("request_session")
                self.stm.send('join')
                self.motion.stop_motion()
                break
            elif key == ord("n"):
                print("No")
                self.stm.send('decline')
                break
            elif timediff >= 10:
                self.stm.send('timeout_motion')
                #self.motion.stop_motion()
                break
    """         
    def stop_video(self):
        keyboard = Controller()
        keyboard.press('q')
        keyboard.release('q')
    """
   
    def request_wait(self):
        print("requested by other party")
        print(1)
        timer = time.perf_counter()
        while True:
            new_time = time.perf_counter()
            timediff = new_time - timer
            try:
                #if keyboard.read_key == 'y':
                if answer == 'yes':
                    print('accepted')
                    myclient.send("accepted")
                    self.stm.send('accept_request')
           
                #elif keyboard.read_key == 'n':
                elif answer == 'no':
                    print("decline")
                    self.stm.send('decline_request')
                    break
                elif timediff >= 10:
                    self.stm.send('timeout_request')
                    #self.motion.stop_motion()
                    break
            except:
                break
                
    #def start_timer(self, t):
        #starts timer
        #print("start timer")
        
        
    #if yes on session_option then call start_session  
    def start_session(self):
        #starte the google meeting
        print("staring session...")
        meet_detector = googleMeet.meeting()
        meet_detector.start()
    
    #call motion_detection when stopping the session. 
    def stop_session(self):
        #stops the video stream
        print("stop video")
    
    def request_user(self):
        #ask if user wants to play game, need both parties to accept the game request.
        print("check if user want ot play game")
    
    #if yes from both users then call the start game option
    def start_game(self):
        print("you are playing cool game :O")
        
    def stop_game(self):
        #stops the game
        print("stoping game...")
    
    #do not need to diplay a actual leaderboard if we do not have time to implement it.
    def display(self):
        #displays the leaderboard on screen
        print("displaying..")
        
    def close_leaderboard(self):
        #close the leaderboard
        print("closing leaderboard")
        


# initial transition
t0 = {"source": "initial",
      "target": "idle",
      "effect": "on_init; motion_detection"}

#The session_option function ask the user if it wants to join a session
t1 = {
    "trigger": "detect",
    "source": "idle",
    "target": "motion_detection",
    "effect": "session_option",
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
    "effect": "motion_detection"
}

t4 = {
    "trigger": "timeout_motion",
    "source": "motion_detection",
    "target": "idle",
    "effect": "motion_detection"
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

t13 = {
    "trigger": "request",
    "source": "idle",
    "target": "requesting",
    "effect": "request_wait",
}

t14 = {
    "trigger": "accept_request",
    "source": "requesting",
    "target": "active",
    "effect": "start_session",
    }

t15 = {
    "trigger": "decline_request",
    "source": "requesting",
    "target": "idle",
    "effect": "motion_detection",
    }

t16 = {
    "trigger": "timeout_request",
    "source": "requesting",
    "target": "idle",
    "effect": "motion_detection",
    }

class MQTT_client:
    motionStatus = True
    
    def __init__(self):
        self.count = 0
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("on_connect(): {}".format(mqtt.connack_string(rc)))

    def on_message(self, client, userdata, msg):
        if msg.topic == "ttm4115/3/comms/client1":
            print(f"on_message(): topic: {msg.topic}:{str(msg.payload)}")
        
        #self.stm_driver.send("message", "tick_tock")
            if str(msg.payload.decode("utf-8")) == "request_session":
                print("session requested")
                #video.stop_video()
                video.stm.send("request")
                video.get_motion()
                
            
    def get_motion_status(self):
        if self.motionStatus:
            return True
        return False
    
    def start(self, broker, port):
        print("Connecting to {}:{}".format(broker, port))
        self.client.connect(broker, port)

        self.client.subscribe("ttm4115/3/comms/client1")

        try:
            # line below should not have the () after the function!
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()
            
    def send(self, message):
        self.client.publish("ttm4115/3/comms/client2", message)

broker, port = "mqtt.item.ntnu.no", 1883

video = Video_Session()
video_chat_machine = Machine(transitions=[t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16], obj=video, name="video_chat")
video.stm = video_chat_machine

driver = Driver()
driver.add_machine(video_chat_machine)

myclient = MQTT_client()
video.mqtt_client = myclient.client
myclient.stm_driver = driver

driver.start()
myclient.start(broker, port)


