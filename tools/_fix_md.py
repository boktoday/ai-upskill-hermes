"""Replace md_blocks in render.py with a clean, correct implementation."""
import pathlib
import re

p = pathlib.Path('C:/Users/insig/figures/upskill-hermes/tools/render.py')
src = p.read_text(encoding='utf-8')

start = src.index('def md_blocks(')
end = src.index('def split_lesson(')

new = '''def md_blocks(md, steps_in=None):
    """Markdown -> HTML. Paragraphs join across soft line breaks; blocks flush the buffer."""
    lines = md.split('\\n')
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append('<p>%s</p>' % inline(' '.join(para)))
            para.clear()

    def is_block(s):
        return (s.startswith((':::', '```', '|', '> ', '#### ', '### '))
                or re.match(r'^- \\[[ x]\\]\\s', s) or re.match(r'^[-*]\\s', s)
                or re.match(r'^\\d+\\.\\s', s) or s in ('---', '***'))

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
            out.append('<div class="callout %s">%s%s</div>' % (cls, head, md_blocks('\\n'.join(body))))
            continue

        if s.startswith('```'):
            flush()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i])
                i += 1
            i += 1
            out.append('<pre><code>%s</code></pre>' % html.escape('\\n'.join(code)))
            continue

        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\\|[\\s\\-:|]+\\|$', lines[i + 1].strip()):
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

        if re.match(r'^- \\[[ x]\\]\\s', s):
            flush()
            items = []
            while i < len(lines) and re.match(r'^- \\[[ x]\\]\\s', lines[i].strip()):
                items.append(re.sub(r'^- \\[[ x]\\]\\s+', '', lines[i].strip()))
                i += 1
            out.append('<ul class="checklist">%s</ul>' % ''.join('<li>%s</li>' % inline(x) for x in items))
            continue

        if re.match(r'^[-*]\\s', s):
            flush()
            items = []
            while i < len(lines) and re.match(r'^[-*]\\s', lines[i].strip()) and not re.match(r'^- \\[[ x]\\]\\s', lines[i].strip()):
                items.append(re.sub(r'^[-*]\\s+', '', lines[i].strip()))
                i += 1
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % inline(x) for x in items))
            continue

        if re.match(r'^\\d+\\.\\s', s):
            flush()
            items = []
            while i < len(lines) and re.match(r'^\\d+\\.\\s', lines[i].strip()):
                items.append(re.sub(r'^\\d+\\.\\s+', '', lines[i].strip()))
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
            out.append('<blockquote>%s</blockquote>' % md_blocks('\\n'.join(buf)))
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
    return '\\n'.join(out)


'''

src = src[:start] + new + src[end:]
p.write_text(src, encoding='utf-8')
print('replaced md_blocks; length now', len(src))
