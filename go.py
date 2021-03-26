#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from time import sleep


options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu') 
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
prefs = {  
    'profile.default_content_setting_values' :  {  
        'notifications' : 2  
    }  
}  
options.add_experimental_option('prefs',prefs)

driver = webdriver.Chrome("./chromedriver", options=options)
driver.get("https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx")


try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "MainBar_lbnUserName")))
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    driver.switch_to.frame("iframeGoURL")
    surveyURLs = [i.get_attribute('href') for i in driver.find_elements_by_partial_link_text('卷-')]
    for i in surveyURLs:
        driver.get(i)
        taExist = driver.find_element_by_id("2150_1").get_attribute("checked")
        table = driver.find_element_by_id("tbQ")
        rating = table.find_elements_by_tag_name("table")
        allBoxes = [f"{i.get_attribute('id')}_0" for i in rating]
        taExistBox = ["2150_0", "1423_0", "1424_0"]
        if taExist:
            boxes = list(filter(lambda a: a not in taExistBox, allBoxes))
        else:
            boxes = allBoxes
        print(f"{boxes}, {taExist}")
        for i in boxes:
            driver.find_element_by_id(i).click()
        sleep(2)
        
except TimeoutException:
    print('等待逾時！')
    driver.close()
    
finally:
    driver.close()