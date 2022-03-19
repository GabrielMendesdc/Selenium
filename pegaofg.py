import re
import shutil
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

pasta = 'C://Users/gabriel/Desktop/ofertas/'

profile=webdriver.ChromeOptions()
# profile.set_preference("browser.download.folderList",2)
# profile.set_preference("browser.download.manager.showWhenStarting",False)
# profile.set_preference("browser.download.dir",pasta)
# profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream")
profile.add_argument("--window-size=1920,1080")
profile.add_argument('--disable-dev-shm-usage')
profile.add_argument('--disable-gpu')
profile.add_argument('--headless')

def pegaofg():
    #ajustando preferencias
    dc = DesiredCapabilities.CHROME
    dc['goog:loggingPrefs'] = { 'browser':'ALL' }
    browser = webdriver.Chrome (ChromeDriverManager().install(),desired_capabilities=dc, options=profile)
    #abre site
    browser.get ("https://www.goodbom.com.br/tabloides/index.php/goodbom-taquaral/")
    #pega o log
    log = browser.get_log('browser')
    links = re.findall('http://\S*?\.jpg', str(log))
    print()
    print()
    for i in links:
        #pula link antigo
        if str(i) != 'http://goodbom.com.br/tabloides/wp-content/uploads/2016/06/mad.jpg':
            print(i)
            response = requests.get(i, stream=True)
            #salva a imagem
            with open(f'C://Users/gabriel/Desktop/ofertas/Goodbom/jpg{links.index(i)}.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
    browser.quit()