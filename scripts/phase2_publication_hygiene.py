from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raven-trace.github.io/raventrace-my"
LOCAL_PHOTO = f"{BASE}/assets/photos/sprm-hq-putrajaya.jpg"
WIKI_PHOTO_RE = re.compile(r"https://upload\.wikimedia\.org/wikipedia/commons/(?:thumb/)?3/33/Putrajaya_Malaysia_Anti-Corruption_Commission-01\.jpg(?:/[^\"'<>)\s]+)?")

PUBLIC_ROOTS = [
    ROOT / "index.html",
    ROOT / "about",
    ROOT / "methodology",
    ROOT / "corrections",
    ROOT / "tips",
    ROOT / "news",
    ROOT / "investigations",
]

RCI_STANDALONE = ROOT / "investigations" / "rci-tabung-haji"
PHOTO_CREDIT = (
    '<p class="photo-credit">Foto konteks untuk pratonton sosial: '
    '<a href="https://commons.wikimedia.org/wiki/File:Putrajaya_Malaysia_Anti-Corruption_Commission-01.jpg" '
    'rel="noopener noreferrer">CEphoto, Uwe Aranas / Wikimedia Commons</a> · '
    '<a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="noopener noreferrer">CC BY-SA 3.0</a>. '
    'Foto bangunan SPRM ini bukan foto pertuduhan, suspek atau bukti salah laku.</p>'
)


def public_html_files():
    seen = set()
    for root in PUBLIC_ROOTS:
        if root.is_file():
            files = [root]
        elif root.exists():
            files = root.rglob("*.html")
        else:
            continue
        for path in files:
            if path in seen:
                continue
            seen.add(path)
            yield path


def is_rci_standalone(path: Path) -> bool:
    try:
        rel = path.relative_to(RCI_STANDALONE)
    except ValueError:
        return False
    return len(rel.parts) >= 2 and rel.name == "index.html"


def ensure_head_asset(text: str, marker: str, html: str) -> str:
    if marker in text:
        return text
    return text.replace("</head>", f"{html}\n</head>", 1)


def ensure_twitter_image(text: str) -> str:
    if 'name="twitter:image"' in text:
        return text
    match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"[^>]*>', text)
    if not match:
        return text
    tag = f'<meta name="twitter:image" content="{match.group(1)}">'
    return text.replace(match.group(0), match.group(0) + tag, 1)


def add_photo_credit(text: str) -> str:
    if LOCAL_PHOTO not in text or "Foto konteks untuk pratonton sosial" in text:
        return text
    if "</main>" in text:
        return text.replace("</main>", f"{PHOTO_CREDIT}\n</main>", 1)
    return text


def sweep(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original

    # Public information architecture: the main Siasatan navigation always opens the desk.
    text = text.replace(
        'href="/raventrace-my/investigations/rci-tabung-haji/">Siasatan</a>',
        'href="/raventrace-my/investigations/">Siasatan</a>',
    )

    # Self-host the licensed SPRM building photo used by social-preview metadata.
    text = WIKI_PHOTO_RE.sub(LOCAL_PHOTO, text)
    text = ensure_twitter_image(text)
    text = add_photo_credit(text)

    if is_rci_standalone(path):
        # Cache-bust the former factual-mutation controller. v2 is interaction-only.
        text = text.replace("raven-section.js?v=1.0.0", "raven-section.js?v=2.0.0")
        text = ensure_head_asset(
            text,
            "data-raven-site-integrity",
            '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-site-integrity.css?v=1.0.0" data-raven-site-integrity>',
        )
        text = ensure_head_asset(
            text,
            "lytcdn.com/lyt.js",
            '<script async src="https://lytcdn.com/lyt.js?site=7d23381ee4e5"></script>',
        )

    if text != original:
        path.write_text(text, encoding="utf-8")
        print("UPDATED", path.relative_to(ROOT))
        return True
    return False


def update_photo_credits() -> bool:
    path = ROOT / "assets" / "PHOTO_CREDITS.md"
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8")
    text = original
    if "Local production copy:" not in text:
        text = text.replace(
            "- File: Putrajaya Malaysia Anti-Corruption Commission-01.jpg\n",
            "- File: Putrajaya Malaysia Anti-Corruption Commission-01.jpg\n"
            "- Local production copy: `assets/photos/sprm-hq-putrajaya.jpg` (1,280 px Wikimedia derivative; no editorial manipulation beyond Wikimedia resizing)\n",
            1,
        )
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("UPDATED", path.relative_to(ROOT))
        return True
    return False


if __name__ == "__main__":
    count = sum(1 for path in public_html_files() if sweep(path))
    count += int(update_photo_credits())
    print(f"Phase 2 publication hygiene complete: {count} files changed")
