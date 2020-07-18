import pandas as pd
import os
import glob

def get_newest_file(dir):
    list_of_files = glob.iglob(dir)
    filename = max(list_of_files, key=os.path.getmtime)
    return filename

file = get_newest_file(os.path.join('data', 'dok', 'my_decks', '*.csv'))

cards_file = get_newest_file(os.path.join('data', 'dok', 'cards', '*.csv'))


decks = pd.read_csv(file)
cards = pd.read_csv(cards_file)

print(decks.sort_values('Sas Rating', ascending=False)[['Name']])
