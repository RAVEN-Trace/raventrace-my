from pathlib import Path
import re

SITE_ID = "7d23381ee4e5"
SNIPPET = f'<script async src="https://lytcdn.com/lyt.js?site={SITE_ID}"></script>'

root = Path(__file__).resolve().parents[1]
changed = []
skipped = []

for path in sorted(root.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    if "lytcdn.com/lyt.js?site=" in text:
        skipped.append(str(path.relative_to(root)))
        continue
    match = re.search(r"</head\s*>", text, flags=re.IGNORECASE)
    if not match:
        continue
    updated = text[:match.start()] + SNIPPET + "\n" + text[match.start():]
    path.write_text(updated, encoding="utf-8")
    changed.append(str(path.relative_to(root)))

print(f"Lytical tracking installed on {len(changed)} HTML files.")
for item in changed:
    print(f"  + {item}")
if skipped:
    print(f"Already tracked: {len(skipped)} files.")
