from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#import pyautogui as py
import time
 
passcode = "309705"
meet_code = "945 6875 1227"
name = "office1"
 
def join(meet, password):
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
    #driver = webdriver.Chrome('C://software/chromedriver.exe')
    driver.get(' https://NTNU.zoom.us/j/94568751227?pwd=c3JmQWxmWjdWQXU2S2J0SDVOWnRYQT09')
    
    time.sleep(5) #to let the webpage open completely
    driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[2]/h3[2]/span/a").click()
    
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='inputname']").send_keys(name)
 
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='joinBtn']").click()
    
    time.sleep(5)
    #driver.find_element_by_xpath("//*[@id='inputname']").send_keys(name)
    
    #time.sleep(5)
    #driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/form/div/div[4]/div").click()
    
    #time.sleep(2)
    #driver.find_element_by_xpath("//*[@id='wc_agree1']").click()
    #time.sleep(2)
    
    #print("before pass")
    # enter passcode
    #enter_passcode = py.locateCenterOnScreen('passc.png')
    #py.moveTo(enter_passcode)
    #py.click()
    #py.write(passcode)
    #print("after pass")

 
    # join the meeting
    #time.sleep(5)
    #btn = py.locateCenterOnScreen("join.png")
    #py.moveTo(btn)
    #py.click()
 
join(meet_code,passcode)