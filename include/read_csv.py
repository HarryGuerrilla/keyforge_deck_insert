import pandas as pd
import os
import glob

def get_newest_file(dir):
    list_of_files = glob.iglob(dir)
    filename = max(list_of_files, key=os.path.getmtime)
    return filename

def cards(cards_f):
    if cards_file == '':
        cards_file = get_newest_file(os.path.join('data', 'dok', 'cards', '*.csv'))
    else:
        cards_file = cards_f
    try:
        cards = pd.read_csv(cards_file)
    except:
        raise Exception("Unable to read cards file.")

    return cards

def decks(input_file):
    if input_file == '':
        file = get_newest_file(os.path.join('data', 'dok', 'my_decks', '*.csv'))
    else:
        file = input_file
    try:
        decks = pd.read_csv(file)
    except:
        raise Exception("Unable to read deck list.")

    decks = decks.fillna(0)

    return decks
