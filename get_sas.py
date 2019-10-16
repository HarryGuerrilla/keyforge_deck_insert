import requests
from requests.auth import HTTPBasicAuth
from api import keyforge_compendium
from api import decksofkeyforge
import json
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white, black
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPM

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Roboto Mono', 'RobotoMono-Regular.ttf'))

deck_id = 'cd7591d1-1e1c-4fca-884f-f6d280b93269'
deck_dir = os.path.join('decks', deck_id)
filename = os.path.join(deck_dir, deck_id)
pdf = os.path.join(deck_dir, 'tuckbox.pdf')
page_width, page_height = landscape(letter)
scale_factor = 0.36


if os.path.isdir(deck_dir):
    print('deck already saved')
    with open(filename + '_dok', 'r') as f:
        data = f.read()
    with open(filename + '_kc', 'r') as f:
        data_kc = f.read()
else:
    url = 'https://decksofkeyforge.com/public-api/v3/decks/' + deck_id
    r = requests.get(url, headers={'Api-Key': decksofkeyforge['key']})
    os.makedirs(deck_dir, exist_ok=True)
    data = r.text
    with open(filename + '_dok', 'w+') as f:
        f.write(data)

    url = 'https://keyforge-compendium.com/api/v1/decks/' + deck_id
    r = requests.get(url, auth=HTTPBasicAuth(keyforge_compendium['user'], keyforge_compendium['password']))
    data = r.text
    with open(filename + '_kc', 'w+') as f:
        f.write(data)

deck = json.loads(data)['deck']
deck_details = json.loads(data_kc)

print(deck['name'], '\n')

def print_cards(x, y, cards, canvas):
    canvas.setFont("Roboto", 10)
    for card in cards:
        canvas.drawString(x, y, card)
        y -= 10

def render_background(canvas):
    img = ImageReader('assets/insert_bg.png')
    iw, ih = img.getSize()
    top = page_height/scale_factor-ih-0.25*inch/scale_factor
    left = 0.25*inch/scale_factor
    canvas.drawImage('assets/insert_bg.png', left, top, mask='auto')

def render_deck_name(canvas):
    canvas.setFont("Roboto", 8)
    left = -0.4*inch
    top = 4.9*inch
    canvas.rotate(90)
    canvas.drawString(top, left, deck['name'])
    canvas.rotate(-90)

def render_sas(canvas):
    canvas.setFont("Roboto Mono", 20)
    canvas.setStrokeColor(white)
    canvas.setFillColor(white)
    left = 0.85*inch
    top = page_height-1.09*inch
    canvas.drawString(left, top, str(deck['sasRating']))
    canvas.setFont("Roboto Mono", 6)
    top = page_height-0.51*inch
    left = left + 3*mm
    canvas.drawString(left, top, str(deck['cardsRating']))
    top = top - 3.2*mm    
    canvas.drawString(left, top, "+" + str(deck['synergyRating']))
    top = top - 3.4*mm    
    canvas.drawString(left, top, "-" + str(deck['antisynergyRating']))

def  render_card_count(canvas):
    canvas.setFont("Roboto Mono", 6)
    canvas.setStrokeColor(black)
    canvas.setFillColor(black)    
    left = 1.01*inch
    top = page_height-1.38*inch
    canvas.drawString(left,top, str(deck_details['common_count']))
    top = top-3.55*mm
    canvas.drawString(left,top, str(deck_details['uncommon_count']))
    left = left + 8.2*mm
    top = page_height-1.38*inch
    canvas.drawString(left,top, str(deck_details['rare_count']))
    top = top-3.7*mm
    canvas.drawString(left,top, str(deck_details['fixed_count']))
    left = left + 7.8*mm
    top = page_height-1.38*inch
    canvas.drawString(left,top, str(deck_details['maverick_count']))
    top = top-3.7*mm
    canvas.drawString(left,top, str(deck_details['variant_count']))    

c = canvas.Canvas(pdf, pagesize=landscape(letter))
c.scale(scale_factor, scale_factor)
render_background(c)
c.scale(2.78,2.78)
render_deck_name(c)
render_sas(c)
render_card_count(c)
c.showPage()
c.save()
