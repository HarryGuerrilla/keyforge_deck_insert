import urllib.request
import os
from PIL import Image

icons = {
    'brobnar': 'https://cdn.keyforgegame.com/media/houses/Brobnar.png',
    'dis': 'https://cdn.keyforgegame.com/media/houses/Dis.png',
    'logos': 'https://cdn.keyforgegame.com/media/houses/Logos.png',
    'mars': 'https://cdn.keyforgegame.com/media/houses/Mars.png',
    'sanctum': 'https://cdn.keyforgegame.com/media/houses/Sanctum.png',
    'saurian': 'https://cdn.keyforgegame.com/media/houses/Saurian.png',
    'shadows': 'https://cdn.keyforgegame.com/media/houses/Shadows.png',
    'staralliance': 'https://cdn.keyforgegame.com/media/houses/Star_Alliance.png',
    'untamed': 'https://cdn.keyforgegame.com/media/houses/Untamed.png'
}

user_agent_string = ("Mozilla/5.0 (X11; Linux i686) " +
                    "AppleWebKit/537.17 (KHTML, like Gecko) Chrome/" +
                    "24.0.1312.27 Safari/537.17")

dir = os.path.join('assets', 'icons')

for icon in icons:
    image_orig = os.path.join(dir, icon + '.png')
    image_l = os.path.join(dir, icon + '_l.png')
    image_s = os.path.join(dir, icon + '_s.png')

    headers = {
        'User-Agent': user_agent_string
    }

    r = urllib.request.Request(icons[icon], headers=headers)
    with urllib.request.urlopen(r) as response:
        with open(image_orig, 'wb') as f:
            f.write(response.read())

    image = Image.open(image_orig)
    image.thumbnail((83, 83))
    image.save(image_l)

    image = Image.open(image_orig)
    image.thumbnail((48, 48))
    image.save(image_s)
