import urllib.request
import urllib.parse
import json
import os
import time

PICKS = [
    ("Midori Takada", "Through the Looking Glass", "midori-takada-through-the-looking-glass.jpg"),
    ("Hailu Mergia", "Tche Belew", "hailu-mergia-and-the-walias-tche-belew.jpg"),
    ("Laraaji", "Ambient 3 Day of Radiance", "laraaji-ambient-3-day-of-radiance.jpg"),
    ("Mulatu Astatke", "Mulatu of Ethiopia", "mulatu-astatke-mulatu-of-ethiopia.jpg"),
    ("Konono No 1", "Congotronics", "konono-no-1-congotronics.jpg"),
    ("DJ Sprinkles", "Midtown 120 Blues", "dj-sprinkles-midtown-120-blues.jpg"),
    ("Jan Jelinek", "Loop Finding Jazz Records", "jan-jelinek-loop-finding-jazz-records.jpg"),
    ("Huerco S", "For Those of You Who Have Never", "huerco-s-for-those-of-you-who-have-never-and-also-those-who-have.jpg"),
    ("Jlin", "Black Origami", "jlin-black-origami.jpg"),
    ("Equiknoxx", "Bird Sound Power", "equiknoxx-bird-sound-power.jpg"),
    ("Oren Ambarchi", "Hubris", "oren-ambarchi-hubris.jpg"),
    ("Tirzah", "Devotion", "tirzah-devotion.jpg"),
]

OUT_DIR = os.path.join(os.path.dirname(__file__), "assets", "picks")
os.makedirs(OUT_DIR, exist_ok=True)

def fetch_cover(artist, album, filename):
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"  skip (already exists): {filename}")
        return

    query = urllib.parse.urlencode({"term": f"{artist} {album}", "entity": "album", "limit": "5"})
    url = f"https://itunes.apple.com/search?{query}"

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f"  ERROR searching '{artist} - {album}': {e}")
        return

    results = data.get("results", [])
    if not results:
        print(f"  NOT FOUND: {artist} - {album}")
        return

    art_url = results[0].get("artworkUrl100", "")
    if not art_url:
        print(f"  NO ART: {artist} - {album}")
        return

    # bump to 600x600
    art_url = art_url.replace("100x100bb", "600x600bb")

    try:
        urllib.request.urlretrieve(art_url, out_path)
        print(f"  OK: {filename}")
    except Exception as e:
        print(f"  ERROR downloading {art_url}: {e}")

for artist, album, filename in PICKS:
    print(f"{artist} — {album}")
    fetch_cover(artist, album, filename)
    time.sleep(0.3)  # be polite to the API

print("\nDone. Check assets/picks/")
