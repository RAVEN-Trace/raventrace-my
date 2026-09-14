from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

base_link = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-home-v1.css?v=1.0.2" data-raven-home-css>'
v2_link = '<link rel="stylesheet" href="/raventrace-my/assets/css/raven-home-mobile-v2.css?v=2.0.0" data-raven-home-mobile-v2>'
if v2_link not in s:
    if base_link not in s:
        raise SystemExit('Homepage base CSS anchor missing')
    s = s.replace(base_link, base_link + '\n  ' + v2_link, 1)

# Keep static/no-JS routes canonical now that these topics live on dedicated subpages.
replacements = {
    'href="/raventrace-my/investigations/rci-tabung-haji/#sources"': 'href="/raventrace-my/investigations/rci-tabung-haji/sources/"',
    'href="/raventrace-my/investigations/rci-tabung-haji/#updates"': 'href="/raventrace-my/investigations/rci-tabung-haji/updates/"',
    'href="/raventrace-my/investigations/rci-tabung-haji/#people"': 'href="/raventrace-my/investigations/rci-tabung-haji/people/"',
}
for old, new in replacements.items():
    s = s.replace(old, new)

# Version marker makes rendered QA/state inspection explicit.
s = s.replace('data-raven-home="1.0.2"', 'data-raven-home="2.0.0"', 1)

p.write_text(s, encoding='utf-8')

# Static validation.
out = p.read_text(encoding='utf-8')
required = [
    'raven-home-mobile-v2.css?v=2.0.0',
    '/assets/visuals/raven-truth-lens-v1.svg',
]
# The visual is loaded by CSS, so validate it from the CSS source as well.
css = Path('assets/css/raven-home-mobile-v2.css').read_text(encoding='utf-8')
if required[0] not in out:
    raise SystemExit('V2 homepage stylesheet was not injected')
if required[1] not in css:
    raise SystemExit('Truth Lens visual is not wired into homepage CSS')
for stale in ('/#updates"','/#people"','/#sources"'):
    if stale in out:
        raise SystemExit(f'Stale homepage route remains: {stale}')
print('Homepage Mobile + Visual V2 rollout validated')
