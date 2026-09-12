from pathlib import Path

src = Path('scripts/revise_narrative_forensics_nlp_v4_1.py').read_text(encoding='utf-8')
old = "anchor='<script src=\"/raventrace-my/assets/js/raven.js?v=3.0.0\" defer></script>'"
new = "anchor='</body></html>'"
count = src.count(old)
if count != 2:
    raise SystemExit(f'Expected two legacy script anchors in V4.1, found {count}')
src = src.replace(old, new)
exec(compile(src, 'revise_narrative_forensics_nlp_v4_2_runtime.py', 'exec'))
