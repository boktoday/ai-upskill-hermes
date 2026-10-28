"""Sync rewritten modules into the Hermes profile, set the model, copy pages."""
import pathlib
import re
import shutil

BASE = pathlib.Path('C:/Users/insig/figures/upskill-hermes')
PROFILE = pathlib.Path('C:/Users/insig/AppData/Local/hermes/profiles/ai-upskill')
MAP = {1: 'agentic-revolution', 2: 'ai-literacy', 3: 'building-agents', 4: 'strategy-ethics', 5: 'advanced-topics'}

for num, slug in MAP.items():
    src = next(BASE.glob('content/module-%d-*.md' % num))
    dst = PROFILE / 'skills' / slug / 'references' / 'content.md'
    dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
    print('%-18s <- %-34s %6d chars' % (slug, src.name, dst.stat().st_size))

# model: MiniMax flash for the field test
cfg = PROFILE / 'config.yaml'
text = cfg.read_text(encoding='utf-8')
if 'model:' in text:
    text = re.sub(r'model:\n(?:  .*\n)*', 'model:\n  default: MiniMax-M3.1-Flash\n  provider: minimax\n', text)
else:
    text = 'model:\n  default: MiniMax-M3.1-Flash\n  provider: minimax\n' + text
cfg.write_text(text, encoding='utf-8')
print('model set:', cfg.read_text(encoding='utf-8').split('\n')[:3])

# pages
if (PROFILE / 'pages').exists():
    shutil.rmtree(PROFILE / 'pages')
shutil.copytree(BASE / 'pages', PROFILE / 'pages')
print('pages in profile:', len(list((PROFILE / 'pages').glob('*.html'))))
