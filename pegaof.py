import shutil
import os.path
import requests
from pegaofg import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from time import sleep

pasta = 'C://Users/gabriel/Desktop/ofertas/'

profile=webdriver.FirefoxOptions()
profile.set_preference("browser.download.folderList",2)
profile.set_preference("browser.download.manager.showWhenStarting",False)
profile.set_preference("browser.download.dir",pasta)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream")
profile.add_argument("--window-size=1920,1080")
profile.add_argument('--disable-dev-shm-usage')
profile.add_argument('--disable-gpu')
profile.add_argument('--headless')
browser=webdriver.Firefox(options=profile)


def zerapasta(parent):
   for raiz, subpastas, arquivos in os.walk(parent):                                      
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(raiz, arquivo)
            os.unlink(caminho_arquivo)
        for subpasta in subpastas:
            caminho_pasta = os.path.join(raiz, subpasta)
            os.rmdir(caminho_pasta)

dicionario = {
        'Dalbem':'https://www.supermercadosdalben.com.br/ofertas.html',
        'Fartura':'https://www.hortifrutifartura.com.br/wp-content/themes/fartura/images/banner-oferta.png',
        'Goodbom':'https://www.goodbom.com.br/tabloides/index.php/goodbom-taquaral/',
        'Oba':'https://oba.digital/ofertas',
        'Pague Menos':'https://www.superpaguemenos.com.br/tabloide-digital/s',}


def pegaof(dicionario, pasta):
    for mercado,site in dicionario.items():
        sleep(2)
        print(f'\n \n {mercado} : {site}')
        browser.get(site)
        pasta_mercado = f'{pasta}/{mercado}'
        listalink = []
        if os.path.isdir(pasta_mercado): # vemos se este diretorio ja existe
            print(f'zerei {mercado} na {pasta_mercado}') 
            zerapasta(pasta_mercado)
        else:
            os.mkdir(pasta_mercado) #  criamos a pasta caso nao exista
            print (f'Pasta {pasta_mercado} criada com sucesso!')
        if mercado == 'Dalbem':
            lista = []
            az = browser.find_elements(By.TAG_NAME,'a')
            for a in az:
                if a.get_attribute('onclick'):
                    listalink.append(a.get_attribute('onclick'))
            for i in set(listalink):
                try:
                    lista.append(i.split("'")[1])                
                    lista.append(i.split('"')[1])
                except IndexError:
                    pass
            for i in lista:
                print(i)
                response = requests.get(i, stream=True)
                with open(f'C://Users/gabriel/Desktop/ofertas/Dalbem/pdf{lista.index(i)}.pdf', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response


        if mercado == 'Fartura':
            url = 'https://www.hortifrutifartura.com.br/wp-content/themes/fartura/images/banner-oferta.png'
            response = requests.get(url, stream=True)
            if not response:
                continue
            else:
                with open('C://Users/gabriel/Desktop/ofertas/Fartura/img.png', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
            del response


        if mercado == 'Oba':
            contador = 0
            btn = browser.find_element(By.XPATH, '//a[contains(@href,"index.php?regiao=sp")]')
            btn.click()
            listas = []
            listas.append(browser.find_elements(By.TAG_NAME,'img'))
            listas.append(browser.find_elements(By.CLASS_NAME,'item active'))
            for lista in listas:
                for elem in lista:
                    if 'assets' not in str(elem.get_attribute('src')):
                        link = elem.get_attribute('src')
                        print(link)
                        response = requests.get(link, stream=True)
                        with open(f'C://Users/gabriel/Desktop/ofertas/oba/oba{contador}.jpeg', 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                        del response
                        contador += 1


        if mercado == 'Pague Menos':
            xs = WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.ID, "internal")))
            # test = browser.find_elements(By.CLASS_NAME, " pt-br ")
            contador = 0
            for x in xs:
                print(x.get_attribute('id')) #pega href
                teste = x.find_elements(By.CSS_SELECTOR, 'div.col col-sm-4 col-xs-6 align-mobile')
                print(teste)
                filho = x.find_element(By.CLASS_NAME, 'pr')
                print(filho.get_attribute('class'))# filho e pega href
                neto = filho.find_element(By.XPATH, './/*')
                print(neto.get_attribute('id'))# filho do filho e pega href
                bisneto = neto.find_element(By.CLASS_NAME, 'container')
                print(bisneto.get_attribute('class'))
                tataraneto = bisneto.find_element(By.CLASS_NAME, 'float')
                print(tataraneto.get_attribute('class'))
                x2tataraneto = tataraneto.find_element(By.ID, 'tabloides')
                print(x2tataraneto.get_attribute('class'))
                x3tataraneto = x2tataraneto.find_element(By.CLASS_NAME, "center")
                print(x3tataraneto.get_attribute('class'))
                x4tataraneto = x3tataraneto.find_elements(By.TAG_NAME, "div")
                for x4 in x4tataraneto:
                    classe = x4.get_attribute('class')
                    if str(classe).startswith('col') and str(classe)[-6:] != 'hidden':
                        print(classe)
                        filhosdox4 = x4.find_elements(By.TAG_NAME, "div")
                        for f in filhosdox4:
                            netosdox4 = f.find_elements(By.TAG_NAME, "a")
                            for i in netosdox4:
                                print(i.get_attribute('href'))
                                response = requests.get(i.get_attribute('href'), stream=True)
                                with open(f'C://Users/gabriel/Desktop/ofertas/Pague Menos/pg{contador}.pdf', 'wb') as out_file:
                                    shutil.copyfileobj(response.raw, out_file)
                                del response
                                contador += 1

                                
        if mercado == 'Goodbom':
            pegaofg()


pegaof(dicionario,pasta)
