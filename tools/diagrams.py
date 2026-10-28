"""Five diagrams, one per module: dual coding, so each module pairs its words with a picture.

Inline SVG, no external files, no fonts beyond the page's own. Colours come from the course palette.
"""

INK = '#2e2c29'
PINK = '#c2517a'
CREAM = '#f7f2e7'
MUTED = '#6b665e'
LINE = '#d8d2c4'


def _box(x, y, w, h, label, fill=CREAM, stroke=INK, size=13, weight='600', colour=INK):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="0" fill="%s" stroke="%s" stroke-width="1.5"/>'
            '<text x="%d" y="%d" font-size="%d" font-weight="%s" fill="%s" text-anchor="middle">%s</text>'
            % (x, y, w, h, fill, stroke, x + w // 2, y + h // 2 + 5, size, weight, colour, label))


def _arrow(x1, y1, x2, y2, dashed=False):
    d = ' stroke-dasharray="5 4"' if dashed else ''
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"%s '
            'marker-end="url(#ah)"/>' % (x1, y1, x2, y2, INK, d))


def _label(x, y, text, size=10.5, anchor='start', weight='400', colour=MUTED):
    return ('<text x="%d" y="%d" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s">%s</text>'
            % (x, y, size, weight, colour, anchor, text))


HEAD = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % INK)


def module1():
    """The ability ladder: five rungs, ascending, each one more judgement handed over."""
    rungs = [('Retrieve', 'find it'), ('Transform', 'reshape it'), ('Draft', 'first version'),
             ('Decide', 'choose'), ('Act', 'change things')]
    out = ['<svg viewBox="0 0 620 320" role="img" aria-label="The ability ladder">', HEAD]
    out.append(_label(30, 28, 'Where work sits on the ladder', size=12, weight='600', colour=PINK))
    out.append(_label(590, 28, 'more judgement handed over &#8594;', size=10.5, anchor='end'))
    for i, (name, sub) in enumerate(rungs):
        x = 30 + i * 112
        y = 250 - i * 42
        out.append(_box(x, y, 96, 48, name, fill='#f6e7ec' if i == 4 else CREAM,
                        stroke=PINK if i == 4 else INK))
        out.append(_label(x + 48, y + 64, sub, anchor='middle'))
        if i:
            out.append(_arrow(x - 12, y + 40, x - 3, y + 12, dashed=True))
    out.append('</svg>')
    return '\n'.join(out)


def module2():
    """Context pressure: one window, four claimants, and what to do about it."""
    out = ['<svg viewBox="0 0 620 250" role="img" aria-label="Context window pressure">', HEAD]
    out.append(_label(40, 34, 'One window, four claimants', size=12, weight='600', colour=PINK))
    out.append('<rect x="40" y="52" width="540" height="96" fill="#fbf8f1" stroke="%s" stroke-width="1.5"/>' % INK)
    segs = [(40, 150, 'system rules', '#e9e2d2'), (190, 130, 'your files', '#dfe7d6'),
            (320, 180, 'conversation', '#f2e3d2'), (500, 80, 'reply room', '#f6e7ec')]
    for x, w, label, fill in segs:
        out.append('<rect x="%d" y="52" width="%d" height="96" fill="%s" stroke="%s" stroke-width="1"/>' % (x, w, fill, LINE))
        out.append(_label(x + w // 2, 106, label, anchor='middle'))
    out.append(_label(40, 180, 'Add a fifth thing and something falls out. That is context pressure, not a bug.', size=11.5))
    out.append(_label(40, 204, 'Cheapest fix first: summarise the history, narrow the files, then split the job.', size=11))
    out.append('</svg>')
    return '\n'.join(out)


def module3():
    """The agent loop: model asks, tool runs, observation returns, your rule decides."""
    out = ['<svg viewBox="0 0 620 300" role="img" aria-label="The agent loop">', HEAD]
    out.append(_label(40, 30, 'Model, tool, observation, repeat', size=12, weight='600', colour=PINK))
    out.append(_box(240, 44, 140, 46, 'Model'))
    out.append(_box(50, 132, 120, 46, 'Tool'))
    out.append(_box(240, 220, 140, 46, 'Observation'))
    out.append(_box(450, 132, 120, 46, 'Your rule'))
    out.append(_arrow(276, 92, 176, 130))
    out.append(_label(150, 96, 'asks'))
    out.append(_arrow(176, 168, 262, 218))
    out.append(_label(196, 208, 'runs'))
    out.append(_arrow(330, 220, 330, 92))
    out.append(_label(338, 158, 'learns'))
    out.append(_arrow(450, 142, 386, 70))
    out.append(_label(520, 104, 'stops or continues', anchor='middle'))
    out.append(_label(40, 292, 'No stop condition, no loop: that is an agent that spends your money.', size=11.5))
    out.append('</svg>')
    return '\n'.join(out)


def module4():
    """Where AI pays: judgement against repetition."""
    out = ['<svg viewBox="0 0 620 290" role="img" aria-label="Where AI pays">', HEAD]
    out.append('<line x1="80" y1="240" x2="580" y2="240" stroke="%s" stroke-width="1.5"/>' % INK)
    out.append('<line x1="80" y1="240" x2="80" y2="50" stroke="%s" stroke-width="1.5"/>' % INK)
    out.append(_label(330, 266, 'repetition &#8594;', anchor='middle', size=11))
    out.append('<text x="52" y="150" font-size="11" fill="%s" transform="rotate(-90 52 150)" text-anchor="middle">'
               'judgement &#8594;</text>' % MUTED)
    quads = [(80, 50, '#eef1e8', 'Keep human', 'judgement, no repetition', INK),
             (330, 50, '#f6e7ec', 'Orchestrate', 'where the money is', PINK),
             (80, 145, '#fbf8f1', 'Automate whole', 'cheap, low risk', INK),
             (330, 145, '#f3ecdd', 'Draft and check', 'your first win', INK)]
    for x, y, fill, title, sub, colour in quads:
        out.append('<rect x="%d" y="%d" width="250" height="95" fill="%s" stroke="%s" stroke-width="1"/>' % (x, y, fill, LINE))
        out.append(_label(x + 125, y + 38, title, size=12, anchor='middle', weight='600', colour=colour))
        out.append(_label(x + 125, y + 58, sub, anchor='middle'))
    out.append('</svg>')
    return '\n'.join(out)


def module5():
    """Four orchestration patterns, each drawn small and correct."""
    out = ['<svg viewBox="0 0 620 350" role="img" aria-label="Four orchestration patterns">', HEAD]

    out.append(_label(30, 34, 'Pipeline', size=12, weight='600', colour=PINK))
    out.append(_box(30, 46, 52, 38, 'A', size=12))
    out.append(_box(112, 46, 52, 38, 'B', size=12))
    out.append(_box(194, 46, 52, 38, 'C', size=12))
    out.append(_arrow(84, 65, 108, 65))
    out.append(_arrow(166, 65, 190, 65))
    out.append(_label(30, 104, 'produces, checks, publishes'))

    out.append(_label(330, 34, 'Fan-out', size=12, weight='600', colour=PINK))
    out.append(_box(330, 46, 52, 38, 'A', size=12))
    out.append(_box(432, 42, 62, 28, 'B', size=12))
    out.append(_box(432, 78, 62, 28, 'C', size=12))
    out.append(_arrow(384, 60, 428, 55))
    out.append(_arrow(384, 72, 428, 90))
    out.append(_label(330, 126, 'one brief, many workers'))

    out.append(_label(30, 172, 'Critic', size=12, weight='600', colour=PINK))
    out.append(_box(30, 190, 52, 38, 'A', size=12))
    out.append(_box(140, 190, 52, 38, 'B', size=12))
    out.append(_arrow(84, 209, 136, 209))
    out.append(_label(110, 202, 'draft', anchor='middle', size=10))
    out.append('<line x1="140" y1="186" x2="56" y2="186" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4" '
               'marker-end="url(#ah)"/>' % INK)
    out.append(_label(98, 172, 'attack', anchor='middle', size=10))
    out.append(_label(30, 250, 'draft, attack, revise'))

    out.append(_label(330, 172, 'Router', size=12, weight='600', colour=PINK))
    out.append(_box(330, 190, 52, 38, 'A', size=12))
    out.append(_box(432, 182, 62, 28, 'B', size=12))
    out.append(_box(432, 218, 62, 28, 'C', size=12))
    out.append(_arrow(384, 202, 428, 196))
    out.append(_arrow(384, 216, 428, 232, dashed=True))
    out.append(_label(330, 278, 'picks one specialist'))

    out.append(_label(30, 336, 'Start with a pipeline. It is the only one you can debug at two in the morning.', size=11.5))
    out.append('</svg>')
    return '\n'.join(out)


DIAGRAMS = {1: module1, 2: module2, 3: module3, 4: module4, 5: module5}

CAPTIONS = {
    1: 'The ability ladder. Each rung hands the machine more of the decision, and each rung needs more of your judgement around it.',
    2: 'A context window is shared, not unlimited. Pressure is normal; planning for it is the skill.',
    3: 'The loop that makes an agent an agent. Take away the stop condition and it becomes a bill.',
    4: 'Most people automate the bottom left and miss the top right, where the money actually is.',
    5: 'The four patterns worth knowing, drawn small enough to remember.',
}


def figure(num):
    svg = DIAGRAMS[num]()
    return ('<figure class="diagram">\n%s\n<figcaption>%s</figcaption>\n</figure>' % (svg, CAPTIONS[num]))
