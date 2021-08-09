import logging
import sys
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

tweet_cases = ('Información COVID-19 ' + day + ' 🇪🇸\n\n' + '‣ Casos: ' + new_cases + '\n‣ Fallecimientos: ' + new_deaths
               + '\n\n#COVID19España')

tweet_vaccines = ('Información vacunas ' + day + ' 🇪🇸\n\n' + '‣ Vacunas distribuidas: ' + new_distributed + ' (' +
                  diff_distributed_str + ')' + '\n‣ Una dosis: ' + new_first_dose + ' (' + diff_first_dose_str
                  + ')' + '\n‣ Completas: ' + new_completed + ' (' + diff_completed_str + ')' + '\n\n' +
                  'Población inmunizada: {:.2f}%\n\n#COVID19España'.format(percentage_completed))

logging.debug("Starting to generate the cases image")

try:
    generate_cases_image(new_cases, new_deaths)
except OSError:
    logging.error("Couldn't generate the cases image")
else:
    logging.debug("Cases image ready")

logging.debug("Starting to generate the vaccines image")

text_primera_dosis = dot_in_string(str(int(new_first_dose.replace('.', '')))) + ' ({:.2f}%)'.format(percentage_first)
text_completa = new_completed + ' ({:.2f}%)'.format(percentage_completed)

try:
    generate_vaccine_image(percentage_first, text_primera_dosis, percentage_completed, text_completa, day)
except OSError:
    logging.error("Couldn't generate the vaccines image")
else:
    logging.debug("Vaccines image ready")

logging.debug("Tweets ready to send")

# print(tweet_cases)
# print('\n')
# print(tweet_vaccines)

logging.debug("Attempt to send the tweets")

send_tweet(tweet_cases, 'today_cases.jpg')
send_tweet(tweet_vaccines, 'vaccines_today.jpg')
