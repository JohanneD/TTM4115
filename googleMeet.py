# import required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
 
 
def Glogin(mail_address, password):
    # Login Page
    driver.get(
        'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')
 
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
 
    # go to google home page
    driver.get('https://google.com/')
    driver.implicitly_wait(100)
 
 
def turnOffMicCam():
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
 
 
def joinNow():
    # Join meet
    print(1)
    time.sleep(5)
    driver.implicitly_wait(2)
    driver.find_element_by_xpath("/html/body/div[1]/c-wiz/div/div/div[9]/div[3]/div/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/button").click()
    print(1)
 
 
def AskToJoin():
    # Ask to Join meet
    time.sleep(5)
    driver.implicitly_wait(2000)
    driver.find_element_by_css_selector(
        'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
    # Ask to join and join now buttons have same xpaths
 
 
# assign email id and password
mail_address = 'officeonettm4115@gmail.com'
password = 'TTM4115-komsys'
meeting_adress = 'https://meet.google.com/puu-hizz-xpx?pli=1'
 
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
driver = webdriver.Chrome(options=opt)
 
# login to Google account
Glogin(mail_address, password)
 
# go to google meet
driver.get(meeting_adress)
#turnOffMicCam()
# AskToJoin()
joinNow()

while True:
    time.sleep(2)
    print(driver.current_url)
    if driver.current_url != meeting_adress:
        driver.quit()