import logging

logging.basicConfig(filename='covid.log', level=logging.DEBUG)


def dot_in_string(value):
    '''
    Replace ',' with '.' in numbers to be in the Spanish way.

    Parameters
    ----------
    value : str
        Number to add replace to commas.

    Returns
    -------
    value : str
        Number with commas replaced by dots.
    '''
    value = value[0] + '{:,}'.format(int(value[1:])).replace(',', '.')
    return value


def str_with_plus_symbol(value):
    '''
    Convert a number to string and add a '+' symbol if it is greater than zero. There is no need to add the '-' symbol
    as it is already in the integer.

    Parameters
    ----------
    value : int
        Number to be converted to string.

    Returns
    -------
    value : str
        Number converted to string with '+' symbol if necessary.
    '''
    return '+' + str(value) if value >= 0 else str(value)


def read_yesterday_data():
    '''
    Read data from 'yesterday.txt'.

    Returns
    -------
    old_distributed : int
        Number read from 'yesterday.txt' referring to distributed vaccines.
    old_administered : int
        Number read from 'yesterday.txt' referring to administered vaccines.
    old_completed : int
        Number read from 'yesterday.txt' referring to completed vaccines.
    '''
    old_distributed = 0
    old_administered = 0
    old_completed = 0

    try:
        with open('yesterday.txt', 'r') as f:
            lines = f.readlines()

            old_distributed = int(lines[0].strip().replace('.', ''))
            old_administered = int(lines[1].strip().replace('.', ''))
            old_completed = int(lines[2].strip().replace('.', ''))
    except OSError:
        logging.error("Could not read data from 'yesterday.txt'")

    return old_distributed, old_administered, old_completed


def write_in_yesterday(distributed, administered, complete):
    '''
    Write data into 'yesterday.txt'.

    Parameters
    ----------
    distributed : str
        Distributed vaccines to be written in 'yesterday.txt'.
    administered : str
        Administered vaccines to be written in 'yesterday.txt'.
    complete : str
        Completed vaccines to be written in 'yesterday.txt'.
    '''
    try:
        with open('yesterday.txt', 'w') as f:
            f.write(distributed)
            f.write('\n')
            f.write(administered)
            f.write('\n')
            f.write(complete)
            f.write('\n')
    except OSError:
        logging.error("Could not write data into 'yesterday.txt'")


def read_from_last_cases():
    '''
    Get cases and deaths info from last day from file 'last_cases.txt'.

    Returns
    -------
    last_cases : str
        Number of COVID-19 cases in Spain the last day.
    last_cases : str
        Number of COVID-19 deaths in Spain the last day.
    '''
    try:
        with open('last_cases.txt', 'r') as f:
            lines = f.readlines()

            last_cases = lines[0].strip().replace(',', '.')
            last_deaths = lines[1].strip().replace(',', '.')

            return last_cases, last_deaths
    except OSError:
        logging.error("Could not read data from 'last_cases.txt")


def write_last_cases(new_cases, new_deaths):
    '''
    Write cases and deaths info from today in 'last_cases.txt'.

    Parameters
    -------
    new_cases : str
        Number of COVID-19 cases in Spain today.
    new_deaths : str
        Number of COVID-19 deaths in Spain today.
    '''
    try:
        with open('last_cases.txt', 'w') as f:
            f.write(new_cases)
            f.write('\n')
            f.write(new_deaths)
            f.write('\n')
    except OSError:
        logging.error("Could not write data into 'last_cases.txt'")
