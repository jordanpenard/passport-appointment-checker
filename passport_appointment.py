from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import winsound

web_path="https://pastel.diplomatie.gouv.fr/rdvinternet/html-4.02.00/frameset/frameset.html?lcid=2&sgid=173&suid=2"

options = webdriver.ChromeOptions() 
# to supress the error messages/logs and hide the browser
options.add_experimental_option('excludeSwitches', ['enable-logging'])


def log(msg):
    print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()), ":", msg)

def alarm(msg):
    log("Alarm -- " + msg)
    winsound.Beep(1000, 1000)

driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver.exe')
driver.minimize_window()

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
                    
        #driver.close()
        time.sleep(60)

    except Exception as e:
        alarm("Oops! " + str(e) + " occurred, trying again")
        driver.close()