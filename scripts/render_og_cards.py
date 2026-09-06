from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1200, 630
BG = '#080c10'
WHITE = '#f4f6f7'
MUTED = '#aeb8c1'
LINE = '#27323a'
FONT_SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONT_MONO_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'

CARDS = [
    dict(file='jamil-khir-reman-20260906-v1.jpg', accent='#f3b33d', case='RCI-TH-2026', date='6 SEP 2026', kicker='RCI TABUNG HAJI · PENGUATKUASAAN', headline='REMAN TAMAT 6 SEP.\nSTATUS SETERUSNYA\nBELUM DISAHKAN.', status='UNKNOWN · OUTCOME BELUM DISAHKAN', marker='WATCH'),
    dict(file='ketelusan-siasatan-th-20260905-v1.jpg', accent='#32d4ef', case='RCI-TH-2026', date='5 SEP 2026', kicker='RCI TABUNG HAJI · KONTEKS AWAM', headline='BEBERAPA RESPONDEN\nMAHU SIASATAN TH\nLEBIH TELUS.', status='CONTEXT · VOX-POP BUKAN TINJAUAN NASIONAL', marker='CONTEXT'),
    dict(file='madinah-rashid-disputed-20260904-v1.jpg', accent='#ed6b67', case='RCI-TH-2026', date='4 SEP 2026', kicker='RCI TABUNG HAJI · DISPUTED RECORD', headline='DUA VERSI.\nSATU REKOD YANG\nBELUM LENGKAP.', status='DISPUTED · REKOD AWAM BERCANGGAH', marker='DISPUTED'),
    dict(file='reformasi-th-20260903-v1.jpg', accent='#6fd19a', case='RCI-TH-2026', date='3 SEP 2026', kicker='RCI TABUNG HAJI · REFORMASI INSTITUSI', headline='19 DARIPADA 25 SYOR\nDILAPOR SELESAI.\nAKTA BELUM MUKTAMAD.', status='PROCESS · REFORMASI BERJALAN', marker='REFORM'),
    dict(file='thp-bina-court-20260903-v1.jpg', accent='#63c8ff', case='RCI-TH-2026', date='3 SEP 2026', kicker='RCI TABUNG HAJI · MAHKAMAH', headline='DUA BEKAS PENGURUS\nTHP BINA DIDAKWA.', status='DIDAKWA · BELUM SABIT', marker='COURT'),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_head(draw, text, maxw=800, start=58, minsize=38):
    size = start
    while size >= minsize:
        f = font(FONT_BOLD, size)
        if all(draw.textbbox((0, 0), line, font=f)[2] <= maxw for line in text.split('\n')):
            return f
        size -= 2
    return font(FONT_BOLD, minsize)


def render(card, outdir):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    accent = card['accent']
    f_brand = font(FONT_BOLD, 40)
    f_sub = font(FONT_MONO, 15)
    f_top = font(FONT_MONO_BOLD, 17)
    f_kick = font(FONT_MONO_BOLD, 19)
    f_status = font(FONT_MONO_BOLD, 17)
    f_foot = font(FONT_MONO, 15)
    f_mark = font(FONT_BOLD, 38)

    d.rectangle((0, 0, W, 8), fill=accent)
    d.rectangle((56, 52, 64, 118), fill=accent)
    d.text((73, 50), 'RAVEN', font=f_brand, fill=WHITE)
    raven_w = d.textbbox((0, 0), 'RAVEN', font=f_brand)[2]
    d.text((73 + raven_w + 8, 50), '-Trace', font=f_brand, fill=accent)
    d.text((73, 96), 'INDEPENDENT · EVIDENCE-LED · MALAYSIA', font=f_sub, fill=MUTED)

    top = f"{card['case']}  /  {card['date']}"
    top_w = d.textbbox((0, 0), top, font=f_top)[2]
    d.text((1140 - top_w, 69), top, font=f_top, fill=MUTED)
    d.line((56, 142, 1144, 142), fill=LINE, width=2)
    d.line((890, 142, 890, 530), fill=LINE, width=1)

    d.text((56, 174), card['kicker'], font=f_kick, fill=accent)
    headline_font = fit_head(d, card['headline'])
    y = 218
    for line in card['headline'].split('\n'):
        d.text((56, y), line, font=headline_font, fill=WHITE)
        y += headline_font.size + 10

    status_w = d.textbbox((0, 0), card['status'], font=f_status)[2]
    d.rounded_rectangle((56, 458, 56 + status_w + 34, 496), radius=8, fill='#0b1116', outline=accent, width=2)
    d.text((73, 468), card['status'], font=f_status, fill=accent)

    cx, cy = 1018, 324
    for radius, colour in [(108, LINE), (82, accent), (56, LINE)]:
        d.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=colour, width=2)
    d.ellipse((cx - 29, cy - 29, cx + 29, cy + 29), fill=accent)
    mark_w = d.textbbox((0, 0), 'R', font=f_mark)[2]
    d.text((cx - mark_w / 2, cy - 25), 'R', font=f_mark, fill=BG)
    label_w = d.textbbox((0, 0), card['marker'], font=f_top)[2]
    d.text((cx - label_w / 2, 445), card['marker'], font=f_top, fill=accent)

    d.line((56, 530, 1144, 530), fill=LINE, width=2)
    d.text((56, 559), 'NEWS CARD · PUBLIC EXPLAINER', font=f_foot, fill=MUTED)
    d.text((56, 589), 'raven-trace.github.io/raventrace-my', font=f_foot, fill=WHITE)
    publisher = 'by SharulR X(ai) Projects'
    pub_w = d.textbbox((0, 0), publisher, font=f_foot)[2]
    d.text((1144 - pub_w, 559), publisher, font=f_foot, fill=MUTED)

    out = Path(outdir) / card['file']
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, 'JPEG', quality=86, optimize=True, progressive=True, subsampling=1)
    print(f'{out} {out.stat().st_size} bytes')


def main():
    root = Path(__file__).resolve().parents[1]
    outdir = root / 'assets' / 'og'
    for card in CARDS:
        render(card, outdir)


if __name__ == '__main__':
    main()
