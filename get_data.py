import requests
import logging
import re
from bs4 import BeautifulSoup

URL_CASES = 'https://www.worldometers.info/coronavirus/country/spain/'
URL_VACCINES = 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/vacunaCovid19.htm'

logging.basicConfig(filename='covid.log', level=logging.DEBUG)


def get_vaccines():
    '''
    Get data about vaccination in Spain.

    Returns
    -------
    distributed : str
        Number of vaccines distributed to Spain.
    administered : str
        Number of vaccines administered in Spain.
    completed : str
        Number of second doses administered in Spain.
    '''
    re_number = r'.*\"cifra\">(.*)</p>'
    page_vaccines = requests.get(URL_VACCINES)
    soup_vaccines = BeautifulSoup(page_vaccines.content, 'html.parser')

    result_distributed = soup_vaccines.find(class_='banner-coronavirus banner-distribuidas')
    match_distributed = re.match(re_number, str(result_distributed).replace('\n', ''))
    distributed = match_distributed.group(1)

    result_administered = soup_vaccines.find(class_='banner-coronavirus banner-vacunas')
    match_administered = re.match(re_number, str(result_administered).replace('\n', ''))
    administered = match_administered.group(1)

    result_completed = soup_vaccines.find(class_='banner-coronavirus banner-completas')
    match_completed = re.match(re_number, str(result_completed).replace('\n', ''))
    completed = match_completed.group(1)

    return distributed, administered, completed


def get_cases():
    '''
    Get data about new cases and deaths in Spain.

    Returns
    -------
    new_cases : str
        Number of new cases of COVID-19 in Spain.
    new_deaths : str
        Number of new deaths due to COVID-19 in Spain.
    '''
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
