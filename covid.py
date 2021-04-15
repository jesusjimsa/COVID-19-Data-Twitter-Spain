import requests
from bs4 import BeautifulSoup
import re

URL_CASES = 'https://www.worldometers.info/coronavirus/country/spain/'
URL_VACCINES = 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/vacunaCovid19.htm'


def get_vaccines():
    page_vaccines = requests.get(URL_VACCINES)
    soup_vaccines = BeautifulSoup(page_vaccines.content, 'html.parser')

    result_distribuidas = soup_vaccines.find(class_='banner-coronavirus banner-distribuidas')
    match_distriuida = re.match(r'.*\"cifra\">(.*)</p>', result_distribuidas)
    distribuidas = match_distriuida.group(1)
    print(distribuidas)


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

        print(new_cases)
        print(new_deaths)

        return new_cases.replace(',', '.'), new_deaths


new_cases, new_deaths = get_cases()

with open('yesterday.txt', 'w') as f:
    f.write(new_cases)
    f.write('\n')
    f.write(new_deaths)
get_vaccines()
