import requests

def run():
    r = requests.get('http://39.107.38.135/freersackler/FS-7510_24.webp')
    img = r.content
    with open('scripts/test', 'wb') as f:
        f.write(img)
        f.close()