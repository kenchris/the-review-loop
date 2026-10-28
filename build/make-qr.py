#!/usr/bin/env python
"""Writes the two QR-code diagrams (build/diagrams/d10-post.html and d-links.html).
QR codes are drawn dark on a light panel, with a quiet zone, so they scan from a projector.
Needs: pip install segno"""
import io, os, segno

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'diagrams')

POST = 'https://claude.dev/blog/solving-code-review-at-anthropic/'
REPO = 'https://github.com/kenchris/review-loop'
TALK = 'https://kenchris.github.io/the-review-loop-site/'


def qr(url, px):
    """An inline SVG of the QR code, `px` pixels wide, including a 3-module quiet zone."""
    q = segno.make(url, error='m')
    return q.svg_inline(scale=1, border=3, dark='#0B1020', light='#F2F5FA', omitsize=True,
                        svgclass=None, lineclass=None).replace('<svg ', '<svg width="%d" height="%d" shape-rendering="crispEdges" ' % (px, px), 1)


def write(name, body):
    io.open(os.path.join(OUT, name), 'w', encoding='utf8', newline='\n').write(body)


write('d10-post.html', '''<style>
 .pt{position:absolute;left:112px;top:300px;width:1000px}
 .pt .ti{font-size:64px;font-weight:600;letter-spacing:-1.5px;line-height:1.08}
 .pt .au{margin-top:34px;font-size:34px;line-height:1.4;color:#DCE4F5}
 .pt .me{margin-top:22px;font-size:28px;color:var(--muted);line-height:1.45}
 .pt .url{margin-top:40px;display:inline-block;padding:14px 26px;border-radius:14px;background:#0A2230;color:#7BE8FF;font:30px Consolas,'Cascadia Mono',monospace;box-shadow:0 0 0 2px rgba(61,217,255,.5)}
 .qb{position:absolute;left:1260px;top:290px;width:548px;height:548px;border-radius:26px;background:#F2F5FA;box-shadow:0 0 0 3px var(--cyan),0 20px 60px rgba(0,0,0,.45);overflow:hidden}
 .qb svg{display:block}
 .qc{position:absolute;left:1260px;top:858px;width:548px;text-align:center;font-size:30px;color:#C9D3E8}
</style>
<div class="pt">
 <div class="ti">How the Claude Code team does code review</div>
 <div class="au">Addy Osmani, Morgan Westlee Lunt and Qing Wang</div>
 <div class="me">claude.dev blog · 15 October 2026 · a 14 minute read</div>
 <div class="url">claude.dev/blog/solving-code-review-at-anthropic</div>
</div>
<div class="qb">%s</div>
<div class="qc">Scan to read it</div>
''' % qr(POST, 548))

card = lambda x, title, sub, url: (
    '<div class="cd" style="left:%dpx"><div class="qb2">%s</div><div class="ct">%s</div><div class="cs">%s</div></div>' % (x, qr(url, 400), title, sub))
write('d-links.html', '''<style>
 .cd{position:absolute;top:290px;width:520px;text-align:center}
 .qb2{width:400px;height:400px;margin:0 auto;border-radius:22px;background:#F2F5FA;overflow:hidden;box-shadow:0 0 0 3px var(--cyan),0 16px 50px rgba(0,0,0,.4)}
 .qb2 svg{display:block}
 .ct{margin-top:34px;font-size:40px;font-weight:600}
 .cs{margin-top:10px;font-size:26px;color:var(--muted);line-height:1.35}
</style>
%s%s%s
''' % (card(112, 'The post', 'How the Claude Code team does code review<br>claude.dev, 15 October 2026', POST),
       card(700, 'review-loop', 'The skills and scripts<br>github.com/kenchris/review-loop', REPO),
       card(1288, 'This talk', 'The slides as a web page<br>kenchris.github.io/the-review-loop-site', TALK)))
print('wrote d10-post.html and d-links.html')
