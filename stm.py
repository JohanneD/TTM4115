from stmpy import Driver, Machine
from threading import Thread

#import keyboard
import paho.mqtt.client as mqtt
import cv2
import camera_motion as camera
import googleMeet
#from six.moves import input
import time
#from pynput.keyboard import Key, Controller

class Video_Session:
    motion = camera.Detector()
    meet_detector = None
    
    def on_init(self):
        print("starting...")
        #motion = motion_detector.Detector()
        
    def stopping_motion(self):
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
                self.stm.send('decline')
                #self.motion.stop_motion()
                break
    
   
    def request_wait(self):
        print("requested by other party")
        print(1)
        timer = time.perf_counter()
        answer = input("join session? (y/n) ") 
        while True:
            new_time = time.perf_counter()
            timediff = new_time - timer
            try:
                if answer.lower() == "y":
                    print('accepted')
                    myclient.send("accepted")
                    self.stm.send('accept_request')
                    break
                elif answer.lower() == "n":
                    print("decline")
                    self.stm.send('decline_request')
                    break
                elif timediff >= 10:
                    self.stm.send('decline_request')
                    #self.motion.stop_motion()
                    break
            except:
                break
        
        
    #if yes on session_option then call start_session  
    def start_session(self):
        #starte the google meeting
        print("staring session...")
        self.meet_detector = googleMeet.meeting()
        self.meet_detector.start()
        self.options_for_call()
        
    
    def options_for_call(self):
        answer = input("Options for the session: 1: start game  2: close session ")
        if answer == "2":
            self.meet_detector.endMeeting()
            self.stm.send("exit")
        elif answer == "1":
            print("Starting game")
            myclient.send("game_started")
            self.stm.send("play")
            #self.start_game()
        elif answer.upper() == "Y":
            self.stm.send("accept_game")
        elif answer.upper() == "N":
            self.stm.send("decline_game")
        else:
            print("Invalid answer, try again!")
            self.options_for_call()

    def options_for_game(self):
        answer = input("If you want to end the game type exit: ")
        if answer == "exit":
            self.stm.send("stop")
        else:
            print("Invalid answer, try again!")
            self.options_for_call()


    #call motion_detection when stopping the session. 
    def stop_session(self):
        #stops the video stream
        print("stop video")
    
    def request_user(self):
        #ask if user wants to play game, need both parties to accept the game request.
        print("check if user want or play game")
    
    #if yes from both users then call the start game option
    def start_game(self):
        print("you are playing cool game :O")
        self.meet_detector.openUI()
        self.options_for_game()
        
    def stop_game(self):
        #stops the game
        print("stopping game...")
        myclient.send("game_stopped")
        self.meet_detector.closeUI()
        self.options_for_call()

    def game_option(self):
        answer = input("you are requested to join a game. Do you want to join? (Y/N) ")
        if answer.upper() == "Y":
            self.stm.send("accept_game")
        elif answer.upper() == "N":
            self.stm.send("decline_game")


# initial transition
t0 = {"source": "initial",
      "target": "detecting",
      "effect": "on_init; motion_detection"}

#The session_option function ask the user if it wants to join a session
t1 = {
    "trigger": "detect",
    "source": "detecting",
    "target": "wait_video",
    "effect": "session_option",
}

t2 = {
    "trigger": "join",
    "source": "wait_video",
    "target": "session",
    "effect": "start_session",
}

t3 = {
    "trigger": "decline",
    "source": "wait_video",
    "target": "detecting",
    "effect": "motion_detection"
}

t4 = {
    "trigger": "exit",
    "source": "session",
    "target": "detecting",
    "effect": "motion_detection",
}

t5 = {
    "trigger": "play",
    "source": "session",
    "target": "game",
    "effect": "start_game",
}

t6 = {
    "trigger": "stop",
    "source": "game",
    "target": "session",
    "effect": "stop_game",
}

t7 = {
    "trigger": "request_game",
    "source": "session",
    "target": "game_waiting",
    "effect": "",
}

t8 = {
    "trigger": "accept_game",
    "source": "game_waiting",
    "target": "game",
    "effect": "start_game",
}

t9 = {
    "trigger": "decline_game",
    "source": "game_waiting",
    "target": "session",
    "effect": "decline_game_request",
}

t10 = {
    "trigger": "request",
    "source": "detecting",
    "target": "requesting",
    "effect": "request_wait",
}

t11 = {
    "trigger": "accept_request",
    "source": "requesting",
    "target": "session",
    "effect": "start_session",
}

t12 = {
    "trigger": "decline_request",
    "source": "requesting",
    "target": "detecting",
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
        if msg.topic == "ttm4115/3/comms/client2":
            print(f"on_message(): topic: {msg.topic}:{str(msg.payload)}")
        
        #self.stm_driver.send("message", "tick_tock")
            if str(msg.payload.decode("utf-8")) == "request_session":
                print("session requested")
                video.stopping_motion()
                video.stm.send("request")
            if str(msg.payload.decode("utf-8")) == "game_started":
                print('you are requested to join a game. Do you want to join? (Y/N) ')
                video.stm.send("request_game")
            if str(msg.payload.decode("utf-8")) == "game_stopped":
                print('Other Office stopped the game')
                
                
            
    def get_motion_status(self):
        if self.motionStatus:
            return True
        return False
    
    def start(self, broker, port):
        print("Connecting to {}:{}".format(broker, port))
        self.client.connect(broker, port)

        self.client.subscribe("ttm4115/3/comms/client2")

        try:
            # line below should not have the () after the function!
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()
            
    def send(self, message):
        self.client.publish("ttm4115/3/comms/client1", message)

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


