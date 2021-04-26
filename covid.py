import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from twython import Twython
from auth import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET_KEY

URL_CASES = 'https://www.worldometers.info/coronavirus/country/spain/'
URL_VACCINES = 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/vacunaCovid19.htm'
POBLACION_ESP = 47450795    # https://www.ine.es/jaxi/Tabla.htm?path=/t20/e245/p08/l0/&file=02003.px&L=0


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


new_cases, new_deaths = get_cases()

new_distribuidas, new_administradas, new_completas = get_vaccines()

old_cases = 0
old_deaths = 0
old_distribuidas = 0
old_administradas = 0
old_completas = 0

with open('yesterday.txt', 'r') as f:
    lines = f.readlines()

    old_cases = int(lines[0].strip().replace('.', ''))
    old_deaths = int(lines[1].strip().replace('.', ''))
    old_distribuidas = int(lines[2].strip().replace('.', ''))
    old_administradas = int(lines[3].strip().replace('.', ''))
    old_completas = int(lines[4].strip().replace('.', ''))

with open('yesterday.txt', 'w') as f:
    f.write(new_cases)
    f.write('\n')
    f.write(new_deaths)
    f.write('\n')
    f.write(new_distribuidas)
    f.write('\n')
    f.write(new_administradas)
    f.write('\n')
    f.write(new_completas)
    f.write('\n')

diff_cases = int(new_cases.replace('.', '')) - old_cases
diff_deaths = int(new_deaths.replace('.', '')) - old_deaths
diff_distribuidas = int(new_distribuidas.replace('.', '')) - old_distribuidas
diff_administradas = int(new_administradas.replace('.', '')) - old_administradas
diff_completas = int(new_completas.replace('.', '')) - old_completas

diff_cases_str = '+' + str(diff_cases) if diff_cases >= 0 else str(diff_cases)
diff_deaths_str = '+' + str(diff_deaths) if diff_deaths >= 0 else str(diff_deaths)
diff_distribuidas_str = '+' + str(diff_distribuidas) if diff_distribuidas >= 0 else str(diff_distribuidas)
diff_administradas_str = '+' + str(diff_administradas) if diff_administradas >= 0 else str(diff_administradas)
diff_completas_str = '+' + str(diff_completas) if diff_completas >= 0 else str(diff_completas)

porcentaje_completas = (int(new_completas.replace('.', '')) / POBLACION_ESP) * 100

today = date.today()

day = today.strftime("%d/%m/%Y")

tweet_casos = ('Información COVID-19 ' + day + ' 🇪🇸\n\n' + '‣ Casos: ' + new_cases + ' (' + diff_cases_str + ')' +
               '\n‣ Fallecimientos: ' + new_deaths + ' (' + diff_deaths_str + ')\n\n#COVID19España')

tweet_vacunas = ('Información vacunas ' + day + ' 🇪🇸\n\n' + '‣ Vacunas distribuidas: ' + new_distribuidas + ' (' +
                 diff_distribuidas_str + ')' + '\n‣ Administradas: ' + new_administradas + ' (' + diff_administradas_str
                 + ')' + '\n‣ Completas: ' + new_completas + '(' + diff_completas_str + ')' + '\n\n' +
                 'Población inmunizada: {:.2f}%\n\n#COVID19España'.format(porcentaje_completas))

# print(tweet_casos)
# print('\n')
# print(tweet_vacunas)

twitter = Twython(
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

twitter.update_status(status=tweet_casos)
twitter.update_status(status=tweet_vacunas)
