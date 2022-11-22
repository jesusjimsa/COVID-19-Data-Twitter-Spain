"""
Get COVID-19 data from Spain.

Created by Jesús Jiménez Sánchez.
"""
import re
import json
import logging
import requests
from bs4 import BeautifulSoup

URL_CASES = 'https://www.worldometers.info/coronavirus/country/spain/'
URL_VACCINES = 'https://covid-vacuna.app/data/latest.json'
URL_BOOSTER = 'https://covid.ourworldindata.org/data/owid-covid-data.json'

TOTAL_JSON_POSITION = 21

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
    json_vaccines = requests.get(URL_VACCINES, timeout=60)

    with open('latest.json', 'wb') as json_file:
        json_file.write(json_vaccines.content)

    with open('latest.json', 'r') as json_file:
        json_info = json.load(json_file)

    distributed = str(json_info[TOTAL_JSON_POSITION]['dosisEntregadas'])
    administered = str(json_info[TOTAL_JSON_POSITION]['dosisPrimeraDosis'])
    completed = str(json_info[TOTAL_JSON_POSITION]['dosisPautaCompletada'])

    return distributed, administered, completed


def get_boosters():
    '''
    Get data about boooster vaccines in Spain.

    Returns
    -------
    booster_doses : int
        Number of booster doses administered in Spain.
    '''
    json_booster = requests.get(URL_BOOSTER, timeout=60)
    i = 0

    with open('owid-covid-data.json', 'wb') as booster_file:
        booster_file.write(json_booster.content)

    with open('owid-covid-data.json', 'r') as json_file:
        json_info = json.load(json_file)

    while "total_boosters" not in json_info['ESP']['data'][-1 - i]:
        i += 1

    booster_doses = json_info['ESP']['data'][-1 - i]["total_boosters"]

    return booster_doses


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
    page_cases = requests.get(URL_CASES, timeout=60)
    soup_cases = BeautifulSoup(page_cases.content, 'html.parser')

    results_cases = soup_cases.find(id='news_block')

    latest_cases = results_cases.find_all('li', class_='news_li')[0]

    new_cases_re = r'.*<strong>(.*) new cases</strong> and <strong>(.*) new deaths</strong>.*'

    match = re.match(new_cases_re, str(latest_cases))

    if match:
        new_cases = match.group(1)
        new_deaths = match.group(2)

        return new_cases.replace(',', '.'), new_deaths

    return None
