"""Render the AI Upskill course to HTML pages.

Inputs
  lessons : C:/Users/insig/figures/orchestrator-agent-repo/skills/orchestrator-course/references/lesson-*.md
  modules : %LOCALAPPDATA%/hermes/profiles/ai-upskill/skills/*/references/content.md
Output
  pages/index.html, pages/lesson-01..15.html, pages/module-*.html, pages/all.html (printable)

Markdown supported: # title, *meta*, ## sections, ###, ####, paragraphs, lists, ordered steps,
fenced code, tables, blockquotes, - [ ] checklists, :::callout kinds, links, bold and code.
"""
import html
import pathlib
import re

BASE = pathlib.Path('C:/Users/insig/figures/upskill-hermes')
PAGES = BASE / 'pages'
CSS = (BASE / 'design' / 'course.css').read_text(encoding='utf-8')
LESSONS_DIR = pathlib.Path('C:/Users/insig/figures/orchestrator-agent-repo/skills/orchestrator-course/references')
PROFILE = pathlib.Path('C:/Users/insig/AppData/Local/hermes/profiles/ai-upskill')

MODULE_SOURCES = [
    (1, 'agentic-revolution', 'The agentic revolution', 'What agents actually are, and the loop they run'),
    (2, 'ai-literacy', 'AI literacy', 'How models work, prompting, and the limits of context'),
    (3, 'building-agents', 'Building agents', 'Make a working Hermes agent you can hand to someone'),
    (4, 'strategy-ethics', 'Strategy and ethics', 'Where AI pays, where it costs, and where it must not go'),
    (5, 'advanced-topics', 'Advanced topics', 'Multi-agent workflows and orchestration patterns'),
]

MODULE_OF = [(1, 'Position'), (2, 'Position'), (3, 'Position'), (4, 'Position'),
             (5, 'Language'), (6, 'Language'), (7, 'Language'),
             (8, 'Build'), (9, 'Build'), (10, 'Build'),
             (11, 'Guardrails'), (12, 'Guardrails'),
             (13, 'Work'), (14, 'Work'), (15, 'Work')]

MODULE_BLURB = {
    'Position': 'Know your work, your rules and your plan before you touch a tool.',
    'Language': 'The words, the prompting discipline and the skills that get work done.',
    'Build': 'Make real things: documents, pages, agents, automations.',
    'Guardrails': 'Security, privacy and the judgement about what never leaves the building.',
    'Work': 'Turn the artefacts into a portfolio, a plan and a way to keep earning.',
}


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def parse_callout(lines):
    kind, title = 'note', ''
    head = lines[0].strip()
    m = re.match(r'^:::\s*(\w+)?\s*(.*)$', head)
    if m:
        first = (m.group(1) or '').lower()
        rest = m.group(2).strip()
        if first == 'callout':
            m2 = re.match(r'^(\w+)?\s*(.*)$', rest)
            kind = (m2.group(1) or 'note').lower() if m2 else 'note'
            title = (m2.group(2) or '').strip() if m2 else ''
        else:
            kind = first or 'note'
            title = rest
    body = lines[1:]
    return kind, title, body


def md_blocks(md, steps_in=None):
    """Markdown -> HTML. Paragraphs join across soft line breaks; blocks flush the buffer."""
    lines = md.split('\n')
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append('<p>%s</p>' % inline(' '.join(para)))
            para.clear()

    def is_block(s):
        return (s.startswith((':::', '```', '|', '> ', '#### ', '### '))
                or re.match(r'^- \[[ x]\]\s', s) or re.match(r'^[-*]\s', s)
                or re.match(r'^\d+\.\s', s) or s in ('---', '***'))

    while i < len(lines):
        s = lines[i].strip()

        if not s:
            flush()
            i += 1
            continue

        if s.startswith(':::'):
            flush()
            block = [lines[i]]
            i += 1
            while i < len(lines) and lines[i].strip() != ':::':
                block.append(lines[i])
                i += 1
            i += 1
            kind, title, body = parse_callout(block)
            cls = {'ok': 'ok', 'warn': 'warn', 'pink': 'pink', 'note': ''}.get(kind, '')
            head = '<h4>%s</h4>' % inline(title) if title else ''
            out.append('<div class="callout %s">%s%s</div>' % (cls, head, md_blocks('\n'.join(body))))
            continue

        if s.startswith('```'):
            flush()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i])
                i += 1
            i += 1
            out.append('<pre><code>%s</code></pre>' % html.escape('\n'.join(code)))
            continue

        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i + 1].strip()):
            flush()
            head = [c.strip() for c in s.strip('|').split('|')]
            rows = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            out.append('<div class="tablewrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
                ''.join('<th>%s</th>' % inline(h) for h in head),
                ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c) for c in row) for row in rows)))
            continue

        if re.match(r'^- \[[ x]\]\s', s):
            flush()
            items = []
            while i < len(lines) and re.match(r'^- \[[ x]\]\s', lines[i].strip()):
                items.append(re.sub(r'^- \[[ x]\]\s+', '', lines[i].strip()))
                i += 1
            out.append('<ul class="checklist">%s</ul>' % ''.join('<li>%s</li>' % inline(x) for x in items))
            continue

        if re.match(r'^[-*]\s', s):
            flush()
            items = []
            while i < len(lines) and re.match(r'^[-*]\s', lines[i].strip()) and not re.match(r'^- \[[ x]\]\s', lines[i].strip()):
                items.append(re.sub(r'^[-*]\s+', '', lines[i].strip()))
                i += 1
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % inline(x) for x in items))
            continue

        if re.match(r'^\d+\.\s', s):
            flush()
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                items.append(re.sub(r'^\d+\.\s+', '', lines[i].strip()))
                i += 1
            cls = ' class="steps"' if steps_in else ''
            out.append('<ol%s>%s</ol>' % (cls, ''.join('<li>%s</li>' % inline(x) for x in items)))
            continue

        if s.startswith('> '):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append('<blockquote>%s</blockquote>' % md_blocks('\n'.join(buf)))
            continue

        if s.startswith('#### '):
            flush()
            out.append('<h4>%s</h4>' % inline(s[5:]))
            i += 1
            continue

        if s.startswith('### '):
            flush()
            out.append('<h3>%s</h3>' % inline(s[4:]))
            i += 1
            continue

        if s in ('---', '***'):
            flush()
            out.append('<hr>')
            i += 1
            continue

        # plain text: accumulate, join soft wraps
        para.append(s)
        i += 1

    flush()
    return '\n'.join(out)


def split_lesson(md):
    lines = md.split('\n')
    title = lines[0].lstrip('# ').strip()
    meta, sections, current = '', [], None
    for line in lines[1:]:
        s = line.strip()
        if s.startswith('*') and s.endswith('*') and not meta and not sections:
            meta = s.strip('*').strip()
            continue
        if s.startswith('## '):
            current = {'title': s[3:].strip(), 'lines': []}
            sections.append(current)
            continue
        if current is not None and s:
            current['lines'].append(line)
    return title, meta, sections


def page(title, eyebrow, deck, meta_chips, body, nav='', extra_head=''):
    chips = ''.join('<span>%s</span>' % c for c in meta_chips)
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style>%s</head>
<body>
<header class="masthead"><div class="inner">
  <p class="eyebrow">%s</p>
  <h1>%s</h1>
  %s
  <div class="meta">%s</div>
</div></header>
<main class="wrap">
%s
%s
<p class="foot">AI Upskill, Hermes edition. Converted from the March 2026 course and rewritten for Hermes. Private, local, yours.</p>
</main></body></html>
""" % (html.escape(title), CSS, extra_head, html.escape(eyebrow), html.escape(title),
       ('<p class="deck">%s</p>' % inline(deck)) if deck else '', chips, body, nav)


def build_lesson(num, path, prev_link, next_link):
    md = path.read_text(encoding='utf-8')
    title, meta, sections = split_lesson(md)
    parts, artefact = [], ''
    m = re.search(r'artefact:\s*`?([^`·]+)`?', meta)
    if m:
        artefact = m.group(1).strip()
    for n, sec in enumerate(sections, 1):
        heading = sec['title']
        if heading.lower().startswith('what you are making'):
            parts.append('<p class="lede">%s</p>' % md_blocks('\n'.join(sec['lines'])))
            continue
        body = md_blocks('\n'.join(sec['lines']), steps_in=('your turn' in heading.lower()))
        accent = ' class="act"' if heading.lower().startswith(('your turn', 'the check', 'sealed when')) else ''
        parts.append('<h2%s>%s</h2>\n%s' % (accent, inline(heading), body))
    chips = [meta.replace('·', '&middot;') if False else 'Module <b>%s</b>' % MODULE_OF[num - 1][1],
             'About <b>%s</b>' % (re.search(r'about (\d+) minutes', meta).group(1) + ' min'
                                  if re.search(r'about (\d+) minutes', meta) else '40 min')]
    if artefact:
        chips.append('Artefact <b>%s</b>' % artefact)
    chips.append('Lesson <b>%d of 15</b>' % num)
    nav = '<nav class="lesson-nav">%s</nav>' % (
        ('<a href="%s">&larr; %s</a>' % prev_link if prev_link else '<span></span>') +
        ('<a href="%s" style="text-align:right">%s &rarr;</a>' % next_link if next_link else '<span></span>'))
    out = page(title, 'AI Upskill · Lesson %d' % num, '', chips, '\n'.join(parts), nav)
    (PAGES / ('lesson-%02d.html' % num)).write_text(out, encoding='utf-8')
    return {'num': num, 'title': title, 'meta': meta, 'artefact': artefact,
            'module': MODULE_OF[num - 1][1], 'file': 'lesson-%02d.html' % num}


def build_module(num, slug, title, deck):
    """Module pages: rewritten content if it exists in content/, otherwise the converted profile copy."""
    local = BASE / 'content' / ('module-%d-%s.md' % (num, slug))
    if local.exists():
        md = local.read_text(encoding='utf-8')
    else:
        src = PROFILE / 'skills' / slug / 'references' / 'content.md'
        if not src.exists():
            return None
        md = src.read_text(encoding='utf-8')

    lines = md.split('\n')
    heading = lines[0].lstrip('# ').strip()
    meta, sections, current = '', [], None
    for line in lines[1:]:
        st = line.strip()
        if st.startswith('*') and st.endswith('*') and not meta and not sections:
            meta = st.strip('*').strip()
            continue
        if st.startswith('## '):
            current = {'title': st[3:].strip(), 'lines': []}
            sections.append(current)
            continue
        if current is not None and st:
            current['lines'].append(line)

    parts = []
    for sec in sections:
        body = md_blocks('\n'.join(sec['lines']), steps_in=('your turn' in sec['title'].lower()))
        head = sec['title']
        if head.lower().startswith(('what you are making', 'overview')):
            parts.append('<p class="lede">%s</p>' % body)
            continue
        accent = ' class="act"' if head.lower().startswith(('your turn', 'the check', 'sealed when', 'exercises')) else ''
        parts.append('<h2%s>%s</h2>\n%s' % (accent, inline(head), body))

    mins = re.search(r'about (\d+) minutes', meta)
    chips = ['Module <b>%d of 5</b>' % num,
             'About <b>%s</b>' % (mins.group(1) + ' min' if mins else '45 min')]
    art = re.search(r'artefact:\s*`?([^`·]+)`?', meta)
    if art:
        chips.append('Artefact <b>%s</b>' % art.group(1).strip())
    nav = '<nav class="lesson-nav"><a href="index.html">&larr; Course map</a><a href="index.html" style="text-align:right">All lessons &rarr;</a></nav>'
    out = page(heading, 'AI Upskill · Module %d' % num, deck, chips, '\n'.join(parts), nav)
    fname = 'module-%d-%s.html' % (num, slug)
    (PAGES / fname).write_text(out, encoding='utf-8')
    return {'num': num, 'slug': slug, 'title': heading, 'file': fname, 'chars': len(md)}


def build_index(lessons_info, modules_info):
    tiles = """<div class="tiles">
  <div class="tile"><span class="big">15</span><span class="label">lessons</span></div>
  <div class="tile"><span class="big">5</span><span class="label">modules</span></div>
  <div class="tile"><span class="big">15</span><span class="label">artefacts you keep</span></div>
  <div class="tile"><span class="big">0</span><span class="label">cloud accounts needed</span></div>
</div>"""
    map_html = ['<ul class="map">']
    for module in ('Position', 'Language', 'Build', 'Guardrails', 'Work'):
        items = [l for l in lessons_info if l['module'] == module]
        rows = ''.join('<li><a href="%s">%s</a> <span class="artefact">%s</span></li>'
                       % (l['file'], html.escape(l['title']), html.escape(l['artefact'] or '')) for l in items)
        map_html.append("""<li><div class="module-head"><h3>%s</h3><span>%d lessons</span></div>
<ol>%s</ol><p style="margin:0;padding:0 16px 16px;color:#6B6660;font-size:14px">%s</p></li>"""
                        % (module, len(items), rows, html.escape(MODULE_BLURB[module])))
    map_html.append('</ul>')

    body = """<p class="lede">A course that ends with a portfolio you made yourself, not a certificate.
Fifteen lessons, one artefact each, checked by the agent before anything is marked done.</p>
%s
<h2>How it runs</h2>
<ol class="steps">
<li>You open the lesson page and read it. It takes two minutes, not twenty.</li>
<li>The agent builds the demo in front of you, in your own folder, and says why each choice was made.</li>
<li>You do the same job on your own work. The page tells you exactly what to hand in.</li>
<li>The agent runs the checks against your file and shows you the output. Pass, and the lesson is sealed.</li>
<li>Between lessons, short reviews keep the earlier ones from fading.</li>
</ol>
<div class="callout pink"><h4>The rule that makes this different</h4>
<p>Nothing is marked complete because it sounds finished. The agent opens the file, runs the check and
quotes the result. If your page does not load, the lesson is not passed, and it says so plainly.</p></div>
<h2>The course</h2>
%s
<h2>What you finish with</h2>
<p>A folder of working artefacts: your task table, your rules card, a prompt library, a page you built,
an agent you configured, a workflow that runs without you, a security review, a portfolio and a ninety
day plan. Plus the habits that produced them.</p>
""" % (tiles, '\n'.join(map_html))
    mod_rows = ''.join(
        '<li><a href="%s">%s</a> <span class="artefact">%s</span></li>' % (m['file'], html.escape(m['title']), html.escape(m['deck']))
        for m in modules_info if m)
    body = body.replace('<h2>What you finish with</h2>',
        '<h2>The deeper modules</h2><ul class="map2" style="list-style:none;padding:0;margin:0 0 26px">%s</ul>'
        '<h2>What you finish with</h2>' % mod_rows)

    out = page('AI Upskill', 'AI Upskill · Hermes edition',
               'Learn to orchestrate AI by building fifteen real things, one lesson at a time.',
               ['<span><b>15</b> lessons</span>', '<span><b>5</b> modules</span>',
                '<span><b>Hermes</b> agent</span>', '<span>Offline <b>HTML</b> pages</span>'], body)
    (PAGES / 'index.html').write_text(out, encoding='utf-8')


def main():
    PAGES.mkdir(parents=True, exist_ok=True)
    files = sorted(LESSONS_DIR.glob('lesson-*.md'))
    infos = []
    for idx, f in enumerate(files):
        num = int(re.search(r'lesson-(\d+)', f.name).group(1))
        prev_link = ('lesson-%02d.html' % (num - 1), 'Lesson %d' % (num - 1)) if num > 1 else None
        next_link = ('lesson-%02d.html' % (num + 1), 'Lesson %d' % (num + 1)) if num < len(files) else None
        infos.append(build_lesson(num, f, prev_link, next_link))
    modules = []
    for num, slug, title, deck in MODULE_SOURCES:
        m = build_module(num, slug, title, deck)
        if m:
            m['deck'] = deck
            modules.append(m)
    build_index(infos, modules)
    print('pages built:', len(infos) + len(modules) + 1)
    print('modules:', [(m['num'], m['chars']) for m in modules if m])
    print('index:', PAGES / 'index.html')


if __name__ == '__main__':
    main()
