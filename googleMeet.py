# import required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
 
class meeting:
    def Glogin(self, mail_address, password, driver):
        # Login Page
        driver.get(
            'https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fmeet.google.com%2Fsih-bygt-fgv&sacu=1&hl=en_US&rip=1')
     
        # input Gmail
        driver.find_element_by_id("identifierId").send_keys(mail_address)
        driver.find_element_by_id("identifierNext").click()
        driver.implicitly_wait(10)
     
        # input Password
        driver.find_element_by_xpath(
            '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
        driver.implicitly_wait(10)
        driver.find_element_by_id("passwordNext").click()
        driver.implicitly_wait(10)
        time.sleep(5)
     
        # go to google home page
        #driver.get('https://google.com/')
        driver.implicitly_wait(5000)
        time.sleep(5)
 
 
    def turnOffMicCam(self, driver):
        # turn off Microphone
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="yDmH0d"]/div/div/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div').click()
        driver.implicitly_wait(3000)
     
        # turn off camera
        time.sleep(1)
        driver.find_element_by_xpath(
            '//*[@id="yDmH0d"]/div/div/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
        driver.implicitly_wait(3000)
     
     
    def joinNow(self, driver):
        # Join meet
        print(1)
        time.sleep(5)
        driver.implicitly_wait(2)
        driver.find_element_by_xpath("//*[@id='yDmH0d']/c-wiz/div/div/div[9]/div[3]/div/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/button/span").click()
        print(1)
     
     
    def AskToJoin(self, driver):
        # Ask to Join meet
        time.sleep(5)
        driver.implicitly_wait(2000)
        driver.find_element_by_css_selector(
            'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
        # Ask to join and join now buttons have same xpaths
     
     
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
        driver = webdriver.Chrome(options=opt)
         
        # login to Google account
        self.Glogin(mail_address, password, driver)
         
        # go to google meet
        #driver.get(meeting_adress)
        #turnOffMicCam()
        # AskToJoin()
        self.joinNow(driver)
        
        time.sleep(5)

        while True:
            time.sleep(2)
            print(driver.current_url)
            if driver.current_url != meeting_adress:
                print(2)
                driver.close()
                driver.quit()
                break
            
        return "session ended"
        