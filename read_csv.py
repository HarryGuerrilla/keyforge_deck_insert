import pandas as pd
import os

filename = 'dok-decks-2019-10-14.csv'
file = os.path.join('decks', filename)

decks = pd.read_csv(file)

print(decks.sort_values('Sas Rating', ascending=False)[['Name']])
