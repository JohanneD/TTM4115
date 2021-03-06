# import required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
 
class meeting:

    driver = None 

    def Glogin(self, mail_address, password):
        # Login Page
        self.driver.get(
            'https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fmeet.google.com%2Fsih-bygt-fgv&sacu=1&hl=en_US&rip=1')
     
        # input Gmail
        self.driver.find_element_by_id("identifierId").send_keys(mail_address)
        self.driver.find_element_by_id("identifierNext").click()
        self.driver.implicitly_wait(10)
     
        # input Password
        self.driver.find_element_by_xpath(
            '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("passwordNext").click()
        self.driver.implicitly_wait(10)
        time.sleep(5)
     
        # go to google home page
        self.driver.implicitly_wait(5000)
        time.sleep(5)
     
     
    def joinNow(self):
        # Join meet
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_xpath("//*[@id='yDmH0d']/c-wiz/div/div/div[9]/div[3]/div/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/button/span").click()
     
     
     
    # assign email id and password
    def start(self):
        mail_address = 'officeonettm4115@gmail.com'
        password = 'TTM4115-komsys'
        meeting_adress = 'https://meet.google.com/sih-bygt-fgv'
         
        # create chrome instance
        opt = Options()
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--start-maximized')
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })
        opt.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=opt)
         
        # login to Google account
        self.Glogin(mail_address, password)
         
        # go to google meet
        self.joinNow()
        
        time.sleep(5)

    def endMeeting(self):
        #end meet, closes the browser
        self.driver.close()
        self.driver.quit()
    
    def openUI(self):
        #Open a new tab with the quiz and leaderboard
        self.driver.execute_script('''window.open("https://ttm4115-guiv2.herokuapp.com/index.html#/","_blank");''')

    def closeUI(self):
        #closes only the tab with the quiz
        window_name = self.driver.window_handles[1]
        self.driver.switch_to.window(window_name)
        self.driver.close()
        window_name = self.driver.window_handles[0]
        self.driver.switch_to.window(window_name)
        