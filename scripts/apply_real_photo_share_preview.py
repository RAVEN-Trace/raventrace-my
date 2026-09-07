from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PHOTO = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Putrajaya_Malaysia_Anti-Corruption_Commission-01.jpg/1280px-Putrajaya_Malaysia_Anti-Corruption_Commission-01.jpg"
COMMONS = "https://commons.wikimedia.org/wiki/File:Putrajaya_Malaysia_Anti-Corruption_Commission-01.jpg"
LICENSE = "https://creativecommons.org/licenses/by-sa/3.0/"
STORY = "/raventrace-my/news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/"

def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")

# 1) Share cards on Homepage/Newsroom must resolve to the dedicated story URL.
rel = "assets/js/raven-share.js"
s = read(rel)
s = s.replace("window.__RAVEN_SHARE_V2_2__", "window.__RAVEN_SHARE_V2_3__")
needle = "    'news-2026-09-03-thp-bina-rm72000':'/raventrace-my/news/2026/09/03/thp-bina-rm72000/'\n"
replacement = (
    "    'news-2026-09-03-thp-bina-rm72000':'/raventrace-my/news/2026/09/03/thp-bina-rm72000/',\n"
    f"    'home-2026-09-07-expected-charges':'{STORY}',\n"
    f"    'news-2026-09-07-expected-charges':'{STORY}'\n"
)
if "home-2026-09-07-expected-charges" not in s:
    if needle not in s:
        raise SystemExit("share map insertion point not found")
    s = s.replace(needle, replacement)
write(rel, s)

# 2) Bust runtime cache for the updated share mapper.
rel = "assets/js/raven.js"
s = read(rel).replace("raven-share.js?v=2.2.0", "raven-share.js?v=2.3.0")
write(rel, s)

# 3) Use a real, reusable contextual photograph for the developing-claim story.
rel = "news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/index.html"
s = read(rel)
s = s.replace(
    '<meta property="og:image" content="https://raven-trace.github.io/raventrace-my/assets/art/rci-tabung-haji-hero.webp"><meta name="twitter:card" content="summary_large_image">',
    f'<meta property="og:image" content="{PHOTO}"><meta property="og:image:secure_url" content="{PHOTO}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1280"><meta property="og:image:height" content="853"><meta property="og:image:alt" content="Ibu Pejabat SPRM di Putrajaya. Foto: CEphoto, Uwe Aranas · CC BY-SA 3.0"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{PHOTO}"><meta name="twitter:image:alt" content="Ibu Pejabat SPRM di Putrajaya. Foto: CEphoto, Uwe Aranas · CC BY-SA 3.0">'
)
s = s.replace('content="2026-09-07T23:55:00+08:00">\n<link rel="stylesheet"', 'content="2026-09-08T01:20:00+08:00">\n<link rel="stylesheet"', 1)
# JSON-LD: add the same representative image.
if '"image":[' not in s:
    s = s.replace('"publisher":{"@type":"Organization","name":"RAVEN-Trace Malaysia"}}', f'"publisher":{{"@type":"Organization","name":"RAVEN-Trace Malaysia"}},"image":["{PHOTO}"]}}')
# Replace generic Raven illustration in article body with contextual real photo + mandatory attribution.
s = s.replace(
    '<figure class="story-art"><img src="/raventrace-my/assets/art/rci-tabung-haji-hero.webp" alt="Ilustrasi editorial RAVEN-Trace untuk siasatan RCI Tabung Haji"><figcaption>ILUSTRASI EDITORIAL · Bukan bukti dan bukan foto pertuduhan mahkamah.</figcaption></figure>',
    f'<figure class="story-art"><img src="{PHOTO}" alt="Ibu Pejabat Suruhanjaya Pencegahan Rasuah Malaysia di Putrajaya"><figcaption>FOTO KONTEKS · Ibu Pejabat SPRM, Putrajaya — bukan foto pertuduhan atau bukti salah laku. <a href="{COMMONS}" rel="noopener noreferrer">Photo by CEphoto, Uwe Aranas</a> · <a href="{LICENSE}" rel="noopener noreferrer">CC BY-SA 3.0</a>.</figcaption></figure>'
)
s = s.replace('raven.js?v=3.6.0', 'raven.js?v=3.7.0')
write(rel, s)

# 4) Bust raven.js on main distribution surfaces so the new mapping reaches repeat visitors.
for rel in ["index.html", "news/index.html", "investigations/rci-tabung-haji/index.html"]:
    s = read(rel)
    s = re.sub(r'raven\.js\?v=3\.[0-9]+\.[0-9]+', 'raven.js?v=3.7.0', s)
    write(rel, s)

# 5) Add/refresh image-use policy and credit trail.
credit = f"""# RAVEN-Trace image credits\n\n## SPRM Headquarters, Putrajaya\n\n- File: Putrajaya Malaysia Anti-Corruption Commission-01.jpg\n- Photographer: CEphoto, Uwe Aranas\n- Source: {COMMONS}\n- License: CC BY-SA 3.0 — {LICENSE}\n- Use: contextual editorial photograph for the 7 Sep 2026 developing-claim story and its social preview.\n- Editorial boundary: the photograph depicts SPRM headquarters. It is not presented as a photograph of any charge, suspect action, court event, or proof of wrongdoing.\n\n## Publication policy\n\nFor material news stories, RAVEN-Trace prefers a real photograph with clear reuse rights when it is contextually accurate. If no suitable licensed photograph is available, the fallback is a clearly labelled RAVEN editorial news card. Synthetic images of identifiable people are not used as evidence photography.\n"""
write("assets/PHOTO_CREDITS.md", credit)

# Validation
share = read("assets/js/raven-share.js")
article = read("news/2026/09/07/azeez-jamil-azmi-dijangka-didakwa/index.html")
assert "home-2026-09-07-expected-charges" in share
assert "news-2026-09-07-expected-charges" in share
assert "__RAVEN_SHARE_V2_3__" in share
assert PHOTO in article
assert "Photo by CEphoto, Uwe Aranas" in article
assert "CC BY-SA 3.0" in article
assert "assets/art/rci-tabung-haji-hero.webp" not in article
print("PASS: real-photo social preview + dedicated share URL mapping applied")
