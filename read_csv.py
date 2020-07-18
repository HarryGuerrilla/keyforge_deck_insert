import pandas as pd
import os

filename = 'dok-decks-2020-07-16.csv'
file = os.path.join('decks', filename)

cards_file = os.path.join('decks', 'dok-cards-2020-07-16.csv')


decks = pd.read_csv(file)
cards = pd.read_csv(cards_file)

print(decks.sort_values('Sas Rating', ascending=False)[['Name']])
