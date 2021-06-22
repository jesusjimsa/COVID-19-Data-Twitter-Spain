import requests
import logging
import re
from bs4 import BeautifulSoup

URL_CASES = 'https://www.worldometers.info/coronavirus/country/spain/'
URL_VACCINES = 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/vacunaCovid19.htm'

logging.basicConfig(filename='covid.log', level=logging.DEBUG)


def get_vaccines():
    re_cifra = r'.*\"cifra\">(.*)</p>'
    page_vaccines = requests.get(URL_VACCINES)
    soup_vaccines = BeautifulSoup(page_vaccines.content, 'html.parser')

    result_distribuidas = soup_vaccines.find(class_='banner-coronavirus banner-distribuidas')
    match_distribuida = re.match(re_cifra, str(result_distribuidas).replace('\n', ''))
    distribuidas = match_distribuida.group(1)

    result_administradas = soup_vaccines.find(class_='banner-coronavirus banner-vacunas')
    match_administrada = re.match(re_cifra, str(result_administradas).replace('\n', ''))
    administradas = match_administrada.group(1)

    result_completas = soup_vaccines.find(class_='banner-coronavirus banner-completas')
    match_completa = re.match(re_cifra, str(result_completas).replace('\n', ''))
    completas = match_completa.group(1)

    return distribuidas, administradas, completas


def get_cases():
    page_cases = requests.get(URL_CASES)
    soup_cases = BeautifulSoup(page_cases.content, 'html.parser')

    results_cases = soup_cases.find(id='news_block')

    latest_cases = results_cases.find_all('li', class_='news_li')[0]

    new_cases_re = r'.*<strong>(.*) new cases</strong> and <strong>(.*) new deaths</strong>.*'

    match = re.match(new_cases_re, str(latest_cases))

    if (match):
        new_cases = match.group(1)
        new_deaths = match.group(2)

        return new_cases.replace(',', '.'), new_deaths
