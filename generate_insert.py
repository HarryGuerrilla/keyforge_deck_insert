import requests
import time
from datetime import date
import json
import os
import sys
import getopt
from include.read_csv import decks
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white, black
from reportlab.lib.pagesizes import letter, legal, A4
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPM
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

format = {
    'background': (0*mm,0*mm),
    'deck_name': (124.46*mm,10.16*mm),
    'house_1': (0.9*mm, 75.2*mm),
    'house_2': (0.9*mm, 64.2*mm),
    'house_3': (0.9*mm, 53.2*mm),
    'house_1s': (37.1*mm, 76.6*mm),
    'house_2s': (37.1*mm, 69.9*mm),
    'house_3s': (37.1*mm, 63.2*mm),
    'stars': (7.9*mm, 1.5*mm),
    'name': (4*mm, 1.5*mm),
    'amber_control': (22.7*mm, 41.8*mm),
    'expected_amber': (22.7*mm, 35.6*mm),
    'amber_protection': (22.7*mm, 29.5*mm),
    'artifact_control': (59.3*mm, 41.8*mm),
    'creature_control': (59.3*mm, 35.6*mm),
    'effective_power': (22.7*mm, 23.7*mm),
    'creature_protection': (22.7*mm, 17.5*mm),
    'efficiency': (41*mm, 41.8*mm),
    'disruption': (41*mm, 35.6*mm),
    'bonus_amber': (41*mm, 23.7*mm),
    'key_cheat': (41*mm, 17.5*mm),
    'archive': (41*mm, 11.4*mm),
    'house_cheating': (59.3*mm, 41.8*mm),
    'other': (41*mm, 5.2*mm),
    'actions': (59.3*mm, 23.7*mm),
    'creatures': (59.3*mm, 17.6*mm),
    'artifacts': (59.3*mm, 11.4*mm),
    'upgrades': (59.3*mm, 5.2*mm),
    'card_rating': (15.7*mm, 79.5*mm),
    'synergy': (15.7*mm, 76.1*mm),
    'antisynergy': (15.7*mm, 72.8*mm),
    'sas': (14*mm, 65.2*mm),
    'aerc': (38*mm, 76.9*mm),
    'common': (19.3*mm, 56.9*mm),
    'uncommon': (19.3*mm, 53.4*mm),
    'rare': (27.3*mm, 56.9*mm),
    'special': (27.3*mm, 53.4*mm),
    'maverick': (35.2*mm, 56.9*mm),
    'legacy': (35.2*mm, 53.4*mm),
    'anomaly': (42.4*mm, 56.9*mm),
    'house_1_aerc': (44.7*mm, 78*mm),
    'house_2_aerc': (44.7*mm, 71.4*mm),
    'house_3_aerc': (44.7*mm, 64.7*mm),
    'win_start': (53.67*mm, 74.75*mm),
    'win_diff': (4.2*mm, -4.18*mm),
    'loss_start': (63.1*mm, 74.75*mm),
    'loss_diff': (4.2*mm, -4.18*mm),
    'sas_updated': (72*mm, 1.5*mm),
    'set_icon': (19.8*mm, 3.5*mm),
    'win_tens': (52.5*mm, 79*mm),
    'loss_tens': (66.8*mm, 79*mm)
}

def render_images(deck, canvas, left, top, s):
    # Background
    bg = 'assets/insert_bg.png'
    canvas.drawImage(bg, (left + format['background'][0])/s, (top + format['background'][1])/s, mask='auto')

    # House Logos
    houses = deck['Houses'].split(' | ')
    house1 = "assets/" + houses[0].lower() + "_l.png"
    canvas.drawImage(house1, (left + format['house_1'][0])/s, (top + format['house_1'][1])/s, mask='auto')
    house1s = "assets/" + houses[0].lower() +  "_s.png"
    canvas.drawImage(house1s, (left + format['house_1s'][0])/s, (top + format['house_1s'][1])/s, mask='auto')
    house2 = "assets/" + houses[1].lower() + "_l.png"
    canvas.drawImage(house2, (left + format['house_2'][0])/s, (top + format['house_2'][1])/s, mask='auto')
    house2s = "assets/" + houses[1].lower() + "_s.png"
    canvas.drawImage(house2s, (left + format['house_2s'][0])/s, (top + format['house_2s'][1])/s, mask='auto')
    house3 = "assets/" + houses[2].lower() + "_l.png"
    canvas.drawImage(house3, (left + format['house_3'][0])/s, (top + format['house_3'][1])/s, mask='auto')
    house3s = "assets/" + houses[2].lower() + "_s.png"
    canvas.drawImage(house3s, (left + format['house_3s'][0])/s, (top + format['house_3s'][1])/s, mask='auto')

    # Stars/
    if deck['Sas Percentile'] >= 99.99:
        stars = "assets/5p_star.png"
    elif deck['Sas Percentile'] >= 99.9:
        stars = "assets/5_star.png"
    elif deck['Sas Percentile'] >= 99:
        stars = "assets/4.5_star.png"
    elif deck['Sas Percentile'] >= 90:
        stars = "assets/4_star.png"
    elif deck['Sas Percentile'] >= 75:
        stars = "assets/3.5_star.png"
    elif deck['Sas Percentile'] < 75 and deck['Sas Percentile'] > 25:
        stars = "assets/3_star.png"
    elif deck['Sas Percentile'] <= 25:
        stars = "assets/2.5_star.png"
    elif deck['Sas Percentile'] <= 10:
        stars = "assets/2_star.png"
    elif deck['Sas Percentile'] <= 1:
        stars = "assets/1.5_star.png"
    elif deck['Sas Percentile'] <= 0.1:
        stars = "assets/1_star.png"
    elif deck['Sas Percentile'] <= 0.01:
        stars = "assets/0.5_star.png"
    else:
        start = "assets/0.5_star.png"

    canvas.drawImage(stars, (left + format['stars'][0])/s, (top + format['stars'][1])/s, mask='auto')

    # Set Icon
    icon = 'assets/set_' + deck['Expansion'] + '.png'
    canvas.drawImage(icon, (left + format['set_icon'][0])/s, (top + format['set_icon'][1])/s, mask='auto')

def render_win_loss(deck, canvas, left, top, s):
    wins = int(deck['Wins'])
    win_tens = int((wins-1)/10)*10
    wins = (wins-1) % 10 if wins > 0 else -1
    l = (left + format['win_start'][0])/s
    t = (top + format['win_start'][1])/s

    for x in range(1, wins+2):
        canvas.drawImage('assets/win.png', l, t, mask='auto')
        if x % 2 == 1:
            l += (format['win_diff'][0]/s)
        else:
            t += (format['win_diff'][1]/s)
            l = (left + format['win_start'][0])/s

    losses = int(deck['Losses'])
    loss_tens = int((losses-1)/10)*10
    losses = (losses-1) % 10 if losses > 0 else -1
    l = (left + format['loss_start'][0])/s
    t = (top + format['loss_start'][1])/s

    for x in range(1, losses+2):
        canvas.drawImage('assets/loss.png', l, t, mask='auto')
        if x % 2 == 1:
            l += (format['loss_diff'][0]/s)
        else:
            t += (format['loss_diff'][1]/s)
            l = (left + format['loss_start'][0])/s

    if loss_tens > 0 or win_tens > 0:
        canvas.setFont("Roboto Mono", 24)
        canvas.drawString(
            (left + format['win_tens'][0])*2.78,
            (top + format['win_tens'][1])*2.78,
            str(win_tens).rjust(2)
        )
        canvas.drawString(
            (left + format['loss_tens'][0])*2.78,
            (top + format['loss_tens'][1])*2.78,
            str(loss_tens).rjust(2)
        )

def render_text(deck, canvas, left, top):
    # deck name
    canvas.setStrokeColor(black)
    canvas.setFillColor(black)
    canvas.setFont("Roboto", 9)
    canvas.rotate(90)
    name_parts = deck['Name'].split(' ')
    char_count = 0
    name_line_1 = ""
    name_line_2 = ""
    while len(name_parts) >0:
        char_count += len(name_parts[0] + " ")
        if char_count <= 26:
            name_line_1 += name_parts[0] + " "
        else:
            name_line_2 += name_parts[0] + " "
        name_parts.pop(0)

    canvas.drawString(top + format['name'][1], (left + format['name'][0])*-1, name_line_1)
    canvas.drawString(top + format['name'][1], (left + format['name'][0] + 3*mm)*-1, name_line_2)

    canvas.setFont("Roboto", 7)
    canvas.drawString(
        (top + format['sas_updated'][1]),
        (left + format['sas_updated'][0])*-1,
        "SAS updated: " + str(deck['Last SAS Update'])
    )
    canvas.rotate(-90)

    canvas.setFont("Roboto Mono", 8)
    canvas.drawString(
        left + format['amber_control'][0],
        top + format['amber_control'][1],
        str(round(deck['Amber Control'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['expected_amber'][0],
        top + format['expected_amber'][1],
        str(round(deck['Expected Amber'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['artifact_control'][0],
        top + format['artifact_control'][1],
        str(round(deck['Artifact Control'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['creature_control'][0],
        top + format['creature_control'][1],
        str(round(deck['Creature Control'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['effective_power'][0],
        top + format['effective_power'][1],
        str(round(deck['Effective Power'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['creature_protection'][0],
        top + format['creature_protection'][1],
        str(round(deck['Creature Protection'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['efficiency'][0],
        top + format['efficiency'][1],
        str(round(deck['Efficiency'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['disruption'][0],
        top + format['disruption'][1],
        str(round(deck['Disruption'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['bonus_amber'][0],
        top + format['bonus_amber'][1],
        str(round(deck['Raw Amber'])).rjust(5)
    )
    canvas.drawString(
        left + format['key_cheat'][0],
        top + format['key_cheat'][1],
        str(round(deck['Key Cheat Count'])).rjust(5)
    )
    canvas.drawString(
        left + format['archive'][0],
        top + format['archive'][1],
        str(round(deck['Card Archive Count'])).rjust(5)
    )
    canvas.drawString(
        left + format['other'][0],
        top + format['other'][1],
        str(round(deck['Other'], 2)).rjust(5)
    )
    canvas.drawString(
        left + format['actions'][0],
        top + format['actions'][1],
        str(round(deck['Action Count'])).rjust(5)
    )
    canvas.drawString(
        left + format['creatures'][0],
        top + format['creatures'][1],
        str(round(deck['Creature Count'])).rjust(5)
    )
    canvas.drawString(
        left + format['artifacts'][0],
        top + format['artifacts'][1],
        str(round(deck['Artifact Count'])).rjust(5)
    )
    canvas.drawString(
        left + format['upgrades'][0],
        top + format['upgrades'][1],
        str(round(deck['Upgrade Count'])).rjust(5)
    )

    canvas.setFont("Roboto Mono", 8)
    canvas.drawString(
        left + format['common'][0],
        top + format['common'][1],
        rarities['common'].rjust(2)
    )
    canvas.drawString(
        left + format['uncommon'][0],
        top + format['uncommon'][1],
        rarities['uncommon'].rjust(2)
    )
    canvas.drawString(
        left + format['rare'][0],
        top + format['rare'][1],
        rarities['rare'].rjust(2)
    )
    canvas.drawString(
        left + format['special'][0],
        top + format['special'][1],
        rarities['special'].rjust(2)
    )
    canvas.drawString(
        left + format['maverick'][0],
        top + format['maverick'][1],
        rarities['maverick'].rjust(2)
    )
    canvas.drawString(
        left + format['legacy'][0],
        top + format['legacy'][1],
        rarities['legacy'].rjust(2)
    )
    canvas.drawString(
        left + format['anomaly'][0],
        top + format['anomaly'][1],
        rarities['anomaly'].rjust(2)
    )

    canvas.setFont("Roboto Mono", 20)
    canvas.setStrokeColor(white)
    canvas.setFillColor(white)
    canvas.drawString(
        left + format['sas'][0],
        top + format['sas'][1],
        str(deck['Sas Rating']).rjust(3)
    )

    canvas.setFont("Roboto Mono", 9)
    canvas.drawString(
        left + format['card_rating'][0],
        top + format['card_rating'][1],
        str(deck['Raw Aerc Score']).rjust(3)
    )
    canvas.drawString(
        left + format['synergy'][0],
        top + format['synergy'][1],
        "+" + str(deck['Synergy Rating']).rjust(2)
    )
    canvas.drawString(
        left + format['antisynergy'][0],
        top + format['antisynergy'][1],
        "-" + str(deck['Antisynergy Rating']).rjust(2)
    )
    canvas.setFont("Roboto Mono", 12)
    canvas.drawString(
        left + format['house_1_aerc'][0],
        top + format['house_1_aerc'][1],
        str(round(deck['House 1 SAS'])).rjust(2)
    )
    canvas.drawString(
        left + format['house_2_aerc'][0],
        top + format['house_2_aerc'][1],
        str(round(deck['House 2 SAS'])).rjust(2)
    )
    canvas.drawString(
        left + format['house_3_aerc'][0],
        top + format['house_3_aerc'][1],
        str(round(deck['House 3 SAS'])).rjust(2)
    )

def get_card_rarity_count(deck_id):
    deck_file = os.path.join('data', 'deck_cache', deck_id + '.json')
    if os.path.isfile(deck_file):
        print('deck already saved')
        with open(deck_file, 'r') as f:
            data = json.load(f)
    else:
        url = 'https://www.keyforgegame.com/api/decks/' + deck_id + '/?links=cards'
        print('sleeping...')
        time.sleep(35)
        print('done')
        r = requests.get(url)
        print('downloaded deck')
        data = r.text
        with open(deck_file, 'w+') as f:
            f.write(data)
        data = json.loads(data)

    commons = 0
    uncommons = 0
    rares = 0
    specials = 0
    mavericks = 0
    anomalies = 0
    legacies = 0

    for card in data['data']['_links']['cards']:
        if card in data['data']['set_era_cards']['Anomaly']:
            anomalies += 1

        if card in data['data']['set_era_cards']['Legacy']:
            legacies += 1

        for c in data['_linked']['cards']:
            if c['id'] == card:
                commons += 1 if c['rarity'] == "Common" else 0
                uncommons += 1 if c['rarity'] == "Uncommon" else 0
                rares += 1 if c['rarity'] == "Rare" else 0
                specials += 1 if c['rarity'] == "FIXED" else 0
                mavericks += 1 if c['is_maverick'] == True else 0

    card_count = {
        'common': str(commons),
        'uncommon': str(uncommons),
        'rare': str(rares),
        'special': str(specials),
        'maverick': str(mavericks),
        'anomaly': str(anomalies),
        'legacy': str(legacies)
    }

    return card_count

def main(argv):
    inputfile = ''
    output = os.path.join('inserts', 'inserts_' + date.today().strftime('%Y-%m-%d') + '.pdf')
    deck = ''
    cards = ''
    pagesize = 'letter'

    try:
        opts,  args = getopt.getopt(
            argv,
            "i:o:d:s:",
            ["input=", "output=", "deck=", "pagesize="]
        )
    except getopt.GetoptError:
        print('generate_insert.py -i <inputfile> -o <outputfile> -d <deck> -c <cards> -s <pagesize>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-d", "--deck"):
            deck = arg
        elif opt in ("-s", "--pagesize"):
            pagesize =  arg

    pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto Mono', 'RobotoMono-Regular.ttf'))

    pdf = output
    if pagesize == 'letter':
        pg_size = letter
    elif pagesize == 'legal':
        pg_size = legal
    elif pagesize == 'A4':
        pg_size = A4
    page_width, page_height = landscape(pg_size)

    #print("letter: ", page_width, page_height)
    scale_factor = 0.36

    insert_width = 73.5*mm
    insert_height = 86.5*mm
    margin = 10*mm
    current_width = margin
    current_height = margin
    gutter = 5*mm

    c = canvas.Canvas(pdf, pagesize=landscape(pg_size))

    decks_to_print = decks(inputfile)
    if deck != '':
        decks_to_print = decks_to_print[decks_to_print["Master Vault Link"] == deck]

    for index, deck in decks_to_print.iterrows():
        print(deck['Name'])
        #print(deck['Master Vault Link'])

        if current_width + insert_width + gutter + margin < page_width:
            current_width = current_width
            current_height = current_height
            add_width = insert_width + gutter
            add_height = 0
        elif current_height + ((insert_height + gutter)*2) + margin < page_height:
            current_height = current_height + insert_height + gutter
            current_width = margin
            add_width = insert_width + gutter
            add_height = 0
        else:
            current_width = margin
            current_height = margin
            add_width = insert_width + gutter
            add_height = 0
            c.showPage()

        global rarities
        rarities = get_card_rarity_count(deck['Master Vault Link'].rsplit('/', 1)[-1])
        c.scale(scale_factor, scale_factor) # set dpi to 200 for images
        render_images(deck, c, current_width, current_height, scale_factor)
        render_win_loss(deck, c, current_width, current_height, scale_factor)

        c.scale(2.78,2.78) # go back to default dpi
        render_text(deck, c, current_width, current_height)

        current_width += add_width
        current_height += add_height

    c.showPage()
    c.save()

if __name__ == "__main__":
    main(sys.argv[1:])
