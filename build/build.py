#!/usr/bin/env python
"""Reads slides/*.md and writes one HTML file per slide into build/html/auto/.
Usage: python build.py            (all slides)
       python build.py 5 7 13     (only these slide numbers)
"""
import glob, html, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'build', 'html', 'auto')
DIAG = os.path.join(ROOT, 'build', 'diagrams')
os.makedirs(OUT, exist_ok=True)


# ---------- parsing ----------
def parse_file(path):
    text = io.open(path, encoding='utf8').read().replace('\r\n', '\n')
    slides, cur, key = [], None, None
    for line in text.split('\n'):
        m = re.match(r'^### (\d+)([a-z]?)\s*$', line)
        if m:
            cur = {'n': int(m.group(1)), 'sfx': m.group(2)}
            slides.append(cur)
            key = None
            continue
        if cur is None:
            continue
        if key and (line.startswith('  ') or line == ''):
            if cur[key + '__mode'] == 'block':
                cur[key] += line[2:] + '\n'
            continue
        m = re.match(r'^([a-z_]+):\s?(.*)$', line)
        if m:
            key, val = m.group(1), m.group(2)
            if val == '|':
                cur[key] = ''
                cur[key + '__mode'] = 'block'
            elif val == '':
                cur[key] = []
                cur[key + '__mode'] = 'list'
            else:
                cur[key] = val
                cur[key + '__mode'] = 'line'
                key = None
            continue
        if key and line.startswith('- ') and cur.get(key + '__mode') == 'list':
            cur[key].append(line[2:])
            continue
    for s in slides:
        for k in list(s):
            if k.endswith('__mode'):
                del s[k]
        for k, v in s.items():
            if isinstance(v, str) and k == 'code':
                s[k] = v.rstrip('\n')
    return slides


def load_all():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'slides', '[0-9]*.md'))):
        out += parse_file(p)
    return sorted(out, key=lambda s: (s['n'], s.get('sfx', '')))


# ---------- text helpers ----------
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    return s


def plain(s):
    return re.sub(r'[*`]', '', s)


def head_size(s, big=(88, 76, 66)):
    n = len(plain(s))
    return big[0] if n <= 34 else big[1] if n <= 60 else big[2]


def st_size(s):
    n = len(plain(s))
    return 120 if n <= 40 else 104 if n <= 70 else 92 if n <= 100 else 80


HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<link rel="stylesheet" href="../base.css"><link rel="stylesheet" href="../templates.css"><link rel="stylesheet" href="../diagram.css">'
        '<script src="../base.js"></script>%s</head><body><div class="slide"><div class="grid"></div>')
TAIL = '</div></body></html>'


def tag(s):
    return '<div class="tagpos"><span class="tag">%s</span></div>' % inline(s['tag']) if s.get('tag') else ''


def source(s):
    return '<div class="src" data-edit="source">%s</div>' % inline(s['source']) if s.get('source') else ''


def header(s, size=None):
    h = s['headline']
    sz = size or head_size(h)
    return tag(s) + '<h2 class="head" data-edit="headline" style="font-size:%dpx">%s</h2>' % (sz, inline(h))


# ---------- types ----------
def t_title(s):
    sub = s.get('sub', '')
    js = io.open(os.path.join(ROOT, 'build', 'html', 'web-graph.js'), encoding='utf8').read()
    return (HEAD % '<style>.t-title{position:absolute;left:112px;top:290px;width:1180px;font-size:112px;font-weight:600;letter-spacing:-3px;line-height:1.04}'
            '.t-sub{position:absolute;left:112px;top:640px;width:1000px;font-size:40px;line-height:1.3;color:#C9D3E8}'
            '.t-who{position:absolute;left:112px;bottom:84px;font-size:30px;line-height:1.45}.t-who b{font-weight:600}.t-who span{color:var(--muted)}</style>'
            + '<svg id="web" style="position:absolute;inset:0" width="1920" height="1080" viewBox="0 0 1920 1080"></svg>'
            + '<div class="tagpos" style="top:150px"><span class="tag">%s</span></div>' % inline(s.get('tag', ''))
            + '<h1 class="t-title" data-edit="headline">%s</h1>' % inline(s['headline'])
            + '<div class="t-sub" data-edit="sub">%s</div>' % inline(sub)
            + '<div class="t-who"><b data-edit="who">%s</b><br><span data-edit="affil">%s</span></div>' % (inline(s.get('who', '')), inline(s.get('affil', '')))
            + '<script>' + js + '</script>' + TAIL)


def t_section(s):
    return (HEAD % '' + '<div class="sec-num">%s</div>' % html.escape(s['num'])
            + '<h2 class="sec-head" data-edit="headline">%s</h2>' % inline(s['headline'])
            + '<div class="sec-sub" data-edit="sub">%s</div>' % inline(s.get('sub', '')) + TAIL)


def t_statement(s):
    size = st_size(s['headline'])
    lines = max(1, round(len(plain(s['headline'])) * size * 0.52 / 1560 + 0.45))
    top = 260
    sub_top = top + int(lines * size * 1.04) + 56
    body = tag(s) + '<h2 class="st-head" data-edit="headline" style="font-size:%dpx">%s</h2>' % (size, inline(s['headline']))
    if s.get('sub'):
        body += '<div class="st-sub" data-edit="sub" style="top:%dpx">%s</div>' % (sub_top, inline(s['sub']))
    return HEAD % '' + body + source(s) + TAIL


def t_bignumber(s):
    num = s['number']
    big = 430 if len(num) <= 2 else 340
    unit = s.get('unit', '')
    usz = 200 if unit == '%' else 110
    body = tag(s)
    body += '<div class="bn-num" style="font-size:%dpx">%s<small style="font-size:%dpx">%s</small></div>' % (big, html.escape(num), usz, html.escape(unit))
    body += '<div class="bn-line" data-edit="line">%s</div>' % inline(s['line'])
    if s.get('side'):
        body += '<div class="bn-side" data-edit="side">%s</div>' % inline(s['side'])
    if s.get('bar'):
        l, p, r = [x.strip() for x in s['bar'].split('|')]
        body += '<div class="bn-barwrap"><div class="b" style="width:%s%%">%s</div><div class="h">%s</div></div>' % (p, html.escape(l), html.escape(r))
    return HEAD % '' + body + source(s) + TAIL


COL = {'cyan': 'linear-gradient(90deg,#1C9CC4,#3DD9FF)', 'amber': 'linear-gradient(90deg,#E08A1E,#FFB84D)',
       'violet': 'linear-gradient(90deg,#6A5CE0,#8B7CFF)', 'muted': 'linear-gradient(90deg,#33406A,#4A5A8E)',
       'green': 'linear-gradient(90deg,#27A85A,#4ADE80)'}
CTEXT = {'cyan': '#3DD9FF', 'amber': '#FFB84D', 'violet': '#8B7CFF', 'muted': '#8A97B1', 'green': '#4ADE80'}


def t_bars(s):
    rows = ''
    for it in s['items']:
        label, val, col = [x.strip() for x in it.split('|')]
        rows += ('<div class="bar-row"><div class="bar-label">%s</div><div class="bar-track"><div class="bar-fill" style="width:%s%%;background:%s"></div></div>'
                 '<div class="bar-val" style="color:%s">%s%%</div></div>') % (html.escape(label), val, COL[col], CTEXT[col], val)
    return HEAD % '' + header(s) + '<div class="bars">%s</div>' % rows + source(s) + TAIL


def t_compare(s):
    lc = {'green': '#4ADE80', 'amber': '#FFB84D', 'cyan': '#3DD9FF', 'violet': '#8B7CFF'}
    lcol = lc.get(s.get('left_color', 'violet'))
    rcol = lc.get(s.get('right_color', 'cyan'))

    def box(cls, title, items, col):
        li = ''.join('<li data-edit="%s-%d">%s</li>' % (cls, i, inline(x)) for i, x in enumerate(items))
        return ('<div class="cmp %s" style="--c:%s;box-shadow:0 0 0 2px %s55"><h3 style="color:%s" data-edit="%s-title">%s</h3><ul>%s</ul></div>'
                % (cls, col, col, col, cls, inline(title), li))
    return (HEAD % '' + header(s) + box('l', s['left_title'], s['left'], lcol) + box('r', s['right_title'], s['right'], rcol)
            + source(s) + TAIL)


def t_fourup(s):
    items = s['items']
    cards = ''
    for i, it in enumerate(items):
        parts = [x.strip() for x in it.split('|')]
        if re.fullmatch(r'\d\d', parts[0]):
            n, t, d = parts[0], parts[1], parts[2] if len(parts) > 2 else ''
        else:
            n, t, d = '', parts[0], parts[1] if len(parts) > 1 else ''
        cards += ('<div class="card"><div class="n">%s</div><div class="t" data-edit="t%d">%s</div><div class="d" data-edit="d%d">%s</div></div>'
                  % (html.escape(n), i, inline(t), i, inline(d).replace('/', '/<wbr>') if ' ' not in d else inline(d)))
    return HEAD % '' + header(s) + '<div class="cards">%s</div>' % cards + source(s) + TAIL


KW = r'\b(const|let|var|async|await|return|function|new|if|else|for|of|true|false|null)\b'


def hl(code):
    out = []
    for line in code.split('\n'):
        m = re.match(r'^(\s*)(//.*)$', line)
        if m:
            out.append(html.escape(m.group(1)) + '<span class="c">%s</span>' % html.escape(m.group(2)))
            continue
        esc = html.escape(line, quote=False)
        esc = re.sub(r'(&quot;|")(.*?)(\1)', lambda mm: '<span class="s">"%s"</span>' % mm.group(2), esc)
        esc = re.sub(r"'([^']*)'", lambda mm: '<span class="s">\'%s\'</span>' % mm.group(1), esc)
        esc = re.sub(KW, r'<span class="k">\1</span>', esc)
        esc = re.sub(r'\b([a-zA-Z_]+)(?=\()', r'<span class="f">\1</span>', esc)
        esc = re.sub(r'\b(readOnlyHint|inputSchema|annotations)\b(?=:)', r'<span class="p">\1</span>', esc)
        out.append(esc)
    return '\n'.join(out)


def t_code(s):
    n = s['code'].count('\n') + 1
    size = 36 if n <= 10 else 32 if n <= 12 else 28
    box = '<div class="codebox"><pre style="font-size:%dpx">%s</pre></div>' % (size, hl(s['code']) if s.get('lang') == 'js' else html.escape(s['code'], quote=False))
    cap = '<div class="codecap" data-edit="caption">%s</div>' % inline(s['caption']) if s.get('caption') else ''
    return HEAD % '' + header(s, 66) + box + cap + source(s) + TAIL


def t_table(s):
    rows = s['items']
    hd = [x.strip() for x in rows[0].split('|')]
    t = '<table class="tbl"><tr>%s</tr>' % ''.join('<th>%s</th>' % html.escape(x) for x in hd)
    for i, r in enumerate(rows[1:]):
        c = [x.strip() for x in r.split('|')]
        t += '<tr><td data-edit="r%da">%s</td><td data-edit="r%db">%s</td></tr>' % (i, inline(c[0]), i, inline(c[1]))
    t += '</table>'
    return HEAD % '' + header(s) + t + source(s) + TAIL


def t_timeline(s):
    items = s['items']
    n = len(items)
    span = 1696 - 320
    out = '<div class="tl-line"></div>'
    for i, it in enumerate(items):
        d, tx = [x.strip() for x in it.split('|', 1)]
        x = 112 + int(i * span / max(1, n - 1))
        up = (i % 2 == 0)
        y = 250 if up else 620
        out += ('<div class="tl-item" style="left:%dpx;top:%dpx"><div class="tl-date" data-edit="d%d">%s</div><div class="tl-text" data-edit="t%d">%s</div></div>'
                % (x, y, i, html.escape(d), i, inline(tx)))
        dot_y = 560 - 17
        out += '<div class="tl-dot" style="left:%dpx;top:%dpx;position:absolute"></div>' % (x + 4, dot_y)
    return HEAD % '' + header(s) + out + source(s) + TAIL


def t_video(s):
    return (HEAD % '' + header(s, 66) + '<div class="vframe" data-video="%s"><div class="vtag">Recorded run</div><div class="vplay"></div></div>' % html.escape(s.get('video', ''))
            + '<div class="vcap" data-edit="caption">%s</div>' % inline(s.get('caption', ''))
            + '<div class="vmach" data-edit="machine">%s</div>' % inline(s.get('machine', '')) + TAIL)


def t_diagram(s):
    path = os.path.join(DIAG, s['name'] + '.html')
    frag = io.open(path, encoding='utf8').read() if os.path.exists(path) else '<div style="position:absolute;left:112px;top:320px;font-size:48px;color:#FFB84D">TODO diagram %s</div>' % s['name']
    css = ''
    m = re.search(r'<style>(.*?)</style>', frag, re.S)
    if m:
        css = '<style>%s</style>' % m.group(1)
        frag = frag.replace(m.group(0), '')
    return HEAD % css + header(s) + frag + source(s) + TAIL


def t_screenshot(s):
    try:
        from PIL import Image
    except ImportError:
        Image = None
    img = s['image']
    path = os.path.join(ROOT, 'assets', 'screenshots', img)
    w, h = Image.open(path).size if Image else (1000, 600)
    scale = min(1120 / w, 640 / h, 2.0)
    dw, dh = int(w * scale), int(h * scale)
    body = tag(s) + '<h2 class="head" data-edit="headline" style="font-size:%dpx">%s</h2>' % (head_size(s['headline']), inline(s['headline']))
    body += ('<div class="shotframe" style="width:%dpx;height:%dpx"><img src="../../../assets/screenshots/%s" width="%d" height="%d"></div>'
             % (dw + 24, dh + 24, img, dw, dh))
    if s.get('image2'):
        p2 = os.path.join(ROOT, 'assets', 'screenshots', s['image2'])
        w2, h2 = Image.open(p2).size if Image else (400, 300)
        sc2 = min(520 / w2, 330 / h2, 2.0)
        body += ('<div class="shotinset" style="left:%dpx;top:%dpx"><img src="../../../assets/screenshots/%s" width="%d" height="%d"></div>'
                 % (112 + dw - int(w2 * sc2) // 2, 290 + dh - int(h2 * sc2) // 2, s['image2'], int(w2 * sc2), int(h2 * sc2)))
    right = '<div class="shotcap" data-edit="caption">%s</div>' % inline(s.get('caption', ''))
    for i, c in enumerate(s.get('callouts', [])):
        right += '<div class="shotco"><span>%d</span><div data-edit="co%d">%s</div></div>' % (i + 1, i, inline(c))
    rl = max(1000, 112 + dw + 24 + 80)
    body += '<div class="shotright" style="left:%dpx;width:%dpx">%s</div>' % (rl, 1808 - rl, right)
    return HEAD % '' + body + source(s) + TAIL


TYPES = {k[2:]: v for k, v in globals().items() if k.startswith('t_')}


def main():
    want = {int(x) for x in sys.argv[1:]}
    for s in load_all():
        if want and s['n'] not in want:
            continue
        fn = os.path.join(OUT, '%02d.html' % s['n'])
        io.open(fn, 'w', encoding='utf8', newline='\n').write(TYPES[s['type']](s))
        print('wrote', os.path.basename(fn), s['type'])


if __name__ == '__main__':
    main()
