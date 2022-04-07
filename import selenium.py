from re import I
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.service import Service

from time import sleep

profile=webdriver.FirefoxOptions()
profile.set_preference("browser.download.folderList",2)
profile.set_preference("browser.download.manager.showWhenStarting",False)
profile.set_preference("browser.download.dir","E:\\scripts")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream")
profile.add_argument("--window-size=1920,1080")
profile.add_argument('--disable-dev-shm-usage')
profile.add_argument('--disable-gpu')
# profile.add_argument('--headless')
browser=webdriver.Firefox(options=profile)


def nota(xml):
    #  XML deve ser um arquivo.xml ou um caminho absoluto
    browser.get('https://www.fsist.com.br/converter-xml-nfe-para-danfe')
    sleep(5)
    lista = [(By.ID,"arquivo"),(By.CLASS_NAME,"butenviar"),(By.ID,"msgsim"),(By.ID,"butlink")]
    for x,y in lista:
        elem = browser.find_element(x,y)
        if lista.index((x,y)) == 0:
            elem.send_keys(xml)
        else:
            sleep(1)
            elem.click()
            sleep(1)


nota('E:\\scripts\\xis.xml')
#def purgedir(parent):
#    for root, dirs, files in os.walk(parent):                                      
#        for item in files:
#            filespec = os.path.join(root, item)
#            os.unlink(filespec)