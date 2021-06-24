import logging
import sys
from datetime import date, datetime
from twython import Twython
from twython import TwythonError
from auth import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET_KEY
from get_data import get_vaccines, get_cases
from tweet_image import generate_cases_image, generate_vaccine_image

POBLACION_ESP = 47450795    # https://www.ine.es/jaxi/Tabla.htm?path=/t20/e245/p08/l0/&file=02003.px&L=0

logging.basicConfig(filename='covid.log', level=logging.DEBUG)


def dot_in_string(value):
    value = value[0] + '{:,}'.format(int(value[1:])).replace(',', '.')
    return value


# There is no new info posted on weekends so there is no need to create a tweet
if datetime.today().weekday() in [5, 6]:
    logging.debug("No info needs to be posted on weekends")
    sys.exit()

new_cases, new_deaths = get_cases()

new_distribuidas, new_administradas, new_completas = get_vaccines()

logging.debug("Cases and vaccines obtained")

old_distribuidas = 0
old_administradas = 0
old_completas = 0

with open('yesterday.txt', 'r') as f:
    lines = f.readlines()

    old_distribuidas = int(lines[0].strip().replace('.', ''))
    old_administradas = int(lines[1].strip().replace('.', ''))
    old_completas = int(lines[2].strip().replace('.', ''))

with open('yesterday.txt', 'w') as f:
    f.write(new_distribuidas)
    f.write('\n')
    f.write(new_administradas)
    f.write('\n')
    f.write(new_completas)
    f.write('\n')

logging.debug("Numbers for tomorrow statistics written in yesterday.txt")

diff_distribuidas = int(new_distribuidas.replace('.', '')) - old_distribuidas
diff_administradas = int(new_administradas.replace('.', '')) - old_administradas
diff_completas = int(new_completas.replace('.', '')) - old_completas

# No need to add the '-' symbol as it is already in the integer
diff_distribuidas_str = '+' + str(diff_distribuidas) if diff_distribuidas >= 0 else str(diff_distribuidas)
diff_administradas_str = '+' + str(diff_administradas) if diff_administradas >= 0 else str(diff_administradas)
diff_completas_str = '+' + str(diff_completas) if diff_completas >= 0 else str(diff_completas)

diff_distribuidas_str = dot_in_string(diff_distribuidas_str)
diff_administradas_str = dot_in_string(diff_administradas_str)
diff_completas_str = dot_in_string(diff_completas_str)

porcentaje_primera = (((int(new_administradas.replace('.', '')) - int(new_completas.replace('.', ''))) / POBLACION_ESP)
                      * 100)
porcentaje_completas = (int(new_completas.replace('.', '')) / POBLACION_ESP) * 100

today = date.today()
day = today.strftime("%d/%m/%Y")

tweet_casos = ('Información COVID-19 ' + day + ' 🇪🇸\n\n' + '‣ Casos: ' + new_cases + '\n‣ Fallecimientos: ' + new_deaths
               + '\n\n#COVID19España')

tweet_vacunas = ('Información vacunas ' + day + ' 🇪🇸\n\n' + '‣ Vacunas distribuidas: ' + new_distribuidas + ' (' +
                 diff_distribuidas_str + ')' + '\n‣ Administradas: ' + new_administradas + ' (' + diff_administradas_str
                 + ')' + '\n‣ Completas: ' + new_completas + ' (' + diff_completas_str + ')' + '\n\n' +
                 'Población inmunizada: {:.2f}%\n\n#COVID19España'.format(porcentaje_completas))

logging.debug("Starting to generate the cases image")

try:
    generate_cases_image(new_cases, new_deaths)
except OSError:
    logging.error("Couldn't generate the cases image")
else:
    logging.debug("Cases image ready")

logging.debug("Starting to generate the vaccines image")

text_primera_dosis = dot_in_string(str((int(new_administradas.replace('.', '')) -
                                        int(new_completas.replace('.', ''))))) + ' ({:.2f}%)'.format(porcentaje_primera)
text_completa = new_completas + ' ({:.2f}%)'.format(porcentaje_completas)

try:
    generate_vaccine_image(porcentaje_primera, text_primera_dosis, porcentaje_completas, text_completa, day)
except OSError:
    logging.error("Couldn't generate the vaccines image")
else:
    logging.debug("Vaccines image ready")

logging.debug("Tweets ready to send")

# print(tweet_casos)
# print('\n')
# print(tweet_vacunas)

twitter = Twython(
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

logging.debug("Attempt to send the tweets")

# TODO: This can be done in a function, it's repeating code now

try:
    cases_image = open('today_cases.jpg', 'rb')
    image_ids = twitter.upload_media(media=cases_image)
    cases_image.close()
    twitter.update_status(status=tweet_casos, media_ids=image_ids['media_id'])
except OSError:
    logging.error("Couldn't open the cases image")
except TwythonError as e:
    logging.error("Couldn't send the cases tweet: %s", e)
else:
    logging.debug("Cases tweet sent succesfully")

try:
    vaccine_image = open('vaccines_today.jpg', 'rb')
    image_ids = twitter.upload_media(media=vaccine_image)
    vaccine_image.close()
    twitter.update_status(status=tweet_vacunas)
except OSError:
    logging.error("Couldn't open the vaccines image")
except TwythonError as e:
    logging.error("Couldn't send the vaccines tweet: %s", e)
else:
    logging.debug("Vaccines tweet sent succesfully")
