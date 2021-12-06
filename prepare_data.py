"""
Format COVID-19 information correctly and save it in text files for the next use.

Created by Jesús Jiménez Sánchez.
"""
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
    return f'{int(value):,}'.replace(',', '.')


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
        Number read from 'yesterday.txt' referring to distributed vaccines
    old_administered : int
        Number read from 'yesterday.txt' referring to administered vaccines
    old_completed : int
        Number read from 'yesterday.txt' referring to completed vaccines
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
        Distributed vaccines to be written in 'yesterday.txt'
    administered : str
        Administered vaccines to be written in 'yesterday.txt'
    complete : str
        Completed vaccines to be written in 'yesterday.txt'
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
