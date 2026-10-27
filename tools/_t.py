import sys, pathlib
sys.path.insert(0, 'tools')
import render

t = pathlib.Path('content/module-3-building-agents.md').read_text(encoding='utf-8')
seg = t.split('## Why it matters')[1].split(':::callout')[0]
print('--- source ---')
print(repr(seg[:220]))
print('--- rendered ---')
print(render.md_blocks(seg)[:400])
