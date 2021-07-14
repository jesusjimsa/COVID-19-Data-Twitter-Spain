import logging
from datetime import date, datetime
from time import sleep
from get_data import get_vaccines, get_cases
from tweet_image import generate_cases_image, generate_vaccine_image
from send_tweet import send_tweet
from prepare_data import dot_in_string, str_with_plus_symbol, read_yesterday_data, write_in_yesterday, \
    read_from_last_cases, write_last_cases

POBLACION_ESP = 47450795    # https://www.ine.es/jaxi/Tabla.htm?path=/t20/e245/p08/l0/&file=02003.px&L=0
TWO_HOURS_IN_SECONDS = 60 * 60 * 2
TEN_MINUTES_IN_SECONDS = 60 * 10


logging.basicConfig(filename='covid.log', level=logging.DEBUG)


while True:
    # There is no new info posted on weekends so there is no need to create a tweet
    if datetime.today().weekday() in [5, 6]:
        logging.debug("No info needs to be posted on weekends, going to sleep for six hours")
        sleep(TWO_HOURS_IN_SECONDS * 3)

    new_distributed, new_administered, new_completed = get_vaccines()
    new_cases, new_deaths = get_cases()
    old_cases, old_deaths = read_from_last_cases()

    if old_cases == new_cases and old_deaths == new_deaths:
        logging.debug("No new information was found, going to sleep for ten minutes")
        sleep(TEN_MINUTES_IN_SECONDS)
        continue

    write_last_cases(new_cases, new_deaths)

    logging.debug("Cases and vaccines obtained")

    old_distributed, old_administered, old_completed = read_yesterday_data()

    write_in_yesterday(new_distributed, new_administered, new_completed)

    logging.debug("Numbers for tomorrow statistics written in yesterday.txt")

    diff_distributed = int(new_distributed.replace('.', '')) - old_distributed
    diff_administered = int(new_administered.replace('.', '')) - old_administered
    diff_completed = int(new_completed.replace('.', '')) - old_completed

    diff_distributed_str = dot_in_string(str_with_plus_symbol(diff_distributed))
    diff_administered_str = dot_in_string(str_with_plus_symbol(diff_administered))
    diff_completed_str = dot_in_string(str_with_plus_symbol(diff_completed))

    percentage_first = (((int(new_administered.replace('.', '')) - int(new_completed.replace('.', ''))) / POBLACION_ESP)
                        * 100)
    percentage_completed = (int(new_completed.replace('.', '')) / POBLACION_ESP) * 100

    today = date.today()
    day = today.strftime("%d/%m/%Y")

    tweet_cases = ('Información COVID-19 ' + day + ' 🇪🇸\n\n' + '‣ Casos: ' + new_cases + '\n‣ Fallecimientos: ' +
                   new_deaths + '\n\n#COVID19España')

    tweet_vaccines = ('Información vacunas ' + day + ' 🇪🇸\n\n' + '‣ Vacunas distribuidas: ' + new_distributed + ' (' +
                      diff_distributed_str + ')' + '\n‣ Administradas: ' + new_administered + ' (' +
                      diff_administered_str + ')' + '\n‣ Completas: ' + new_completed + ' (' + diff_completed_str + ')'
                      + '\n\n' + 'Población inmunizada: {:.2f}%\n\n#COVID19España'.format(percentage_completed))

    logging.debug("Starting to generate the cases image")

    try:
        generate_cases_image(new_cases, new_deaths)
    except OSError:
        logging.error("Couldn't generate the cases image")
    else:
        logging.debug("Cases image ready")

    logging.debug("Starting to generate the vaccines image")

    text_primera_dosis = (dot_in_string(str((int(new_administered.replace('.', '')) -
                                             int(new_completed.replace('.', ''))))) +
                          ' ({:.2f}%)'.format(percentage_first))
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

    logging.debug("Going to sleep for two hours")
    sleep(TWO_HOURS_IN_SECONDS)
