"""
Get information about COVID-19 in Spain and send tweets with it.

Created by Jesús Jiménez Sánchez.
"""
import logging
import sys
import json
from time import sleep
from datetime import date, datetime
from get_data import get_vaccines, get_cases
from tweet_image import generate_cases_image, generate_vaccine_image
from send_tweet import send_tweet
from prepare_data import dot_in_string, str_with_plus_symbol, read_yesterday_data, write_in_yesterday

POBLACION_ESP = 47450795    # https://www.ine.es/jaxi/Tabla.htm?path=/t20/e245/p08/l0/&file=02003.px&L=0

logging.basicConfig(filename='covid.log', level=logging.DEBUG)

# There is no new info posted on weekends so there is no need to create a tweet
if datetime.today().weekday() in [5, 6]:
    logging.debug("No info needs to be posted on weekends")
    sys.exit()

new_cases, new_deaths = get_cases()
new_distributed, new_first_dose, new_completed = get_vaccines()

new_distributed = dot_in_string(new_distributed)
new_first_dose = dot_in_string(new_first_dose)
new_completed = dot_in_string(new_completed)

logging.debug("Cases and vaccines obtained")

old_distributed, old_first_dose, old_completed = read_yesterday_data()

write_in_yesterday(new_distributed, new_first_dose, new_completed)

logging.debug("Numbers for tomorrow statistics written in yesterday.txt")

diff_distributed = int(new_distributed.replace('.', '')) - old_distributed
diff_first_dose = int(new_first_dose.replace('.', '')) - old_first_dose
diff_completed = int(new_completed.replace('.', '')) - old_completed

diff_distributed_str = dot_in_string(str_with_plus_symbol(diff_distributed))
diff_first_dose_str = dot_in_string(str_with_plus_symbol(diff_first_dose))
diff_completed_str = dot_in_string(str_with_plus_symbol(diff_completed))

percentage_first = ((int(new_first_dose.replace('.', '')) / POBLACION_ESP) * 100)
percentage_completed = (int(new_completed.replace('.', '')) / POBLACION_ESP) * 100

today = date.today()
day = today.strftime("%d/%m/%Y")

tweet_cases = (
    f'Información COVID-19 {day} 🇪🇸\n\n'
    f'‣ Casos: {new_cases}\n'
    f'‣ Fallecimientos: {new_deaths}\n\n'
    f'#COVID19España #COVID19Data #COVID19Spain'
)

tweet_vaccines = (
    f'Información vacunas {day} 🇪🇸\n\n'
    f'‣ Vacunas distribuidas: {new_distributed} ({diff_distributed_str})\n'
    f'‣ Una dosis: {new_first_dose} ({diff_first_dose_str})\n'
    f'‣ Completas: {new_completed} ({diff_completed_str})\n\n'
    f'Población inmunizada: {percentage_completed:.2f}%\n\n'
    f'#COVID19España #COVID19Data #COVID19Spain'
)

logging.debug("Starting to generate the cases image")

try:
    generate_cases_image(new_cases, new_deaths)
except OSError:
    logging.error("Couldn't generate the cases image")
else:
    logging.debug("Cases image ready")

logging.debug("Starting to generate the vaccines image")

text_first_dose = new_first_dose + f' ({percentage_first:.2f}%)'
text_completed = new_completed + f' ({percentage_completed:.2f}%)'

try:
    generate_vaccine_image(percentage_first, text_first_dose, percentage_completed, text_completed, day)
except OSError:
    logging.error("Couldn't generate the vaccines image")
else:
    logging.debug("Vaccines image ready")

logging.debug("Tweets ready to send")

# print(tweet_cases)
# print('\n')
# print(tweet_vaccines)

logging.debug("Attempt to send the tweets")

send_tweet(tweet_cases, image_path='today_cases.jpg')
tweet_response = send_tweet(tweet_vaccines, image_path='vaccines_today.jpg')

with open('latest.json', 'r') as json_file:
    json_info = json.load(json_file)

for i in range(0, 19):
    community_tweet = (
        f"Vacunación en {json_info[i]['ccaa']}\n\n"
        f"‣ Primera dosis: {dot_in_string(str(json_info[i]['dosisPrimeraDosis']))} "
        f"({(json_info[i]['porcentajePoblacionPrimeraDosis'] * 100):.2f}%)\n"
        f"‣ Segunda dosis: {dot_in_string(str(json_info[i]['dosisPautaCompletada']))} "
        f"({(json_info[i]['porcentajePoblacionCompletas'] * 100):.2f}%)"
    )

    sleep(1)    # Sleep one second to prevent suspension because of spam
    tweet_response = send_tweet(community_tweet, in_reply_to_id=tweet_response['id_str'])
