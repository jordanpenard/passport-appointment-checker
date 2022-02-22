from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import requests
import os
import json

web_path="https://pastel.diplomatie.gouv.fr/rdvinternet/html-4.02.00/frameset/frameset.html?lcid=2&sgid=173&suid=2"

display = Display(visible=0, size=(1920, 1080))
display.start()

options = webdriver.ChromeOptions() 
# to supress the error messages/logs and hide the browser
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

def log(msg):
    print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()), ":", msg)
    f = open("log.txt", "a")
    f.write(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()) + " : " + msg + "\n")
    f.close()
    
def alarm(msg):
    log("Alarm -- " + msg)

    try:
        slack_data = {'text': msg, 'username': "Passport appointment notifier", 'icon_emoji': ":bell:"}
        response = requests.post(os.environ.get('webhook_url'), data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
    except Exception as e:
        log("Couldn't send a slack notification because of " + str(e))
        
driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')

alarm("Passport appointment checker is starting")

while (1):
    try:
        driver.delete_all_cookies()
        driver.get(web_path)

        time.sleep(5)

        driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frame[2]'))
        driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frame[1]'))

        driver.find_element_by_id("item2_0_0").click()
        time.sleep(1)

        driver.switch_to.parent_frame()
        driver.switch_to.frame(driver.find_element_by_xpath('/html/frameset/frame[2]'))
        
        driver.find_element_by_id("ccg").click()        
        time.sleep(1)
        
        driver.find_element_by_id("boutonSuivant_link").click()
        time.sleep(5)

        # Expecting an Alert message if there's no appointments available
        try:
            obj = driver.switch_to.alert
            msg=obj.text
            if (msg != "Actuellement, tous les créneaux pour la démarche 'Dépôt de demande d'inscription, de passeport, de CNIS' sont occupés. Nous vous invitons à réitérer votre demande plus tard."):
                alarm(msg)
            else:
                log("Nothing yet")
            obj.accept()

        except NoAlertPresentException as e:
            alarm("No alert present, looks like appointments may be available : " + web_path)
                    
        time.sleep(60)

    except Exception as e:
        alarm("Oops! " + str(e) + " occurred, trying again")
