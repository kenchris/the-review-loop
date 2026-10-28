#!/usr/bin/env python
"""Turns the transcripts in build/term/*.json into mp4 files in videos/.
The output of every command is real (see capture-term.py); the typing is replayed.
Each state of the terminal is rendered once with headless Chrome, then ffmpeg holds each for its duration.
Usage: python make-term-videos.py [name ...]      (default: all)"""
import glob, html, io, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
WORK = os.path.join(HERE, 'term', 'frames')
CHARS_PER_FRAME = 4          # typing speed: 4 characters per frame at 12 frames per second
TYPE_DT = 1 / 12.0
LINE_DT = 0.06               # output appears line by line
PAUSE_AFTER_OUTPUT = 2.2
PAUSE_BEFORE_TYPING = 0.5

PAGE = '''<!doctype html><meta charset="utf-8"><style>
html,body{margin:0;width:1920px;height:1080px;background:#0B1020;overflow:hidden}
.win{position:absolute;left:112px;top:90px;width:1696px;height:900px;border-radius:18px;background:#0A0F1E;box-shadow:0 0 0 2px #24304F,0 30px 80px rgba(0,0,0,.5);overflow:hidden}
.bar{height:56px;background:#121A33;display:flex;align-items:center;padding:0 22px;gap:12px;font:26px 'Segoe UI',sans-serif;color:#8A97B1}
.dot{width:16px;height:16px;border-radius:50%%;background:#33406A}
pre{margin:0;padding:26px 34px;font:30px/1.38 Consolas,'Cascadia Mono',monospace;color:#E6ECF8;white-space:pre-wrap;word-break:break-word}
.p{color:#4ADE80}.c{color:#7BE8FF}.o{color:#C9D3E8}.f{color:#FF6B7A}.k{color:#4ADE80}.w{color:#FFB84D}.cur{background:#3DD9FF;color:#0A0F1E}
</style><div class="win"><div class="bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span style="margin-left:14px">%s</span></div><pre>%s</pre></div>'''


def colour(line):
    e = html.escape(line, quote=False)
    if re.match(r'^(FAIL|STOP)', line):
        return '<span class="f">%s</span>' % e
    if re.match(r'^\[[a-z-]+\]', line):
        return '<span class="w">%s</span>' % e
    if re.match(r'^(ok|created|ready)\b', line) or 'covered by reports' in line:
        return '<span class="k">%s</span>' % e
    return '<span class="o">%s</span>' % e


def clean(out):
    out = re.sub(r'(?m)^(repository ).*$', r'\1./neon-smash', out)
    out = re.sub(r'(?m)^(review-loop [\d.]+ at ).*$', r'\1~/review-loop', out)
    return out


def states(tr):
    """Yields (html of the terminal, seconds to show it)."""
    done = []                # lines already finished
    def view(extra=''):
        body = ''.join(done) + extra
        return body
    yield view('<span class="p">$ </span><span class="cur"> </span>'), PAUSE_BEFORE_TYPING + 0.4
    for st in tr['steps']:
        cmd = st['cmd']
        for i in range(CHARS_PER_FRAME, len(cmd) + CHARS_PER_FRAME, CHARS_PER_FRAME):
            yield view('<span class="p">$ </span><span class="c">%s</span><span class="cur"> </span>' % html.escape(cmd[:i], quote=False)), TYPE_DT
        done.append('<span class="p">$ </span><span class="c">%s</span>\n' % html.escape(cmd, quote=False))
        yield view(), 0.35
        lines = clean(st['out']).split('\n')
        for ln in lines:
            done.append(colour(ln) + '\n')
            yield view(), LINE_DT
        yield view('<span class="p">$ </span><span class="cur"> </span>'), PAUSE_AFTER_OUTPUT
        done.append('\n')
    yield view('<span class="p">$ </span><span class="cur"> </span>'), 1.5


def build(name):
    tr = json.load(io.open(os.path.join(HERE, 'term', name + '.json'), encoding='utf8'))
    d = os.path.join(WORK, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    lst = []
    prev = None
    for i, (body, dur) in enumerate(states(tr)):
        if body == prev and lst:
            lst[-1][1] += dur
            continue
        prev = body
        hp = os.path.join(d, '%04d.html' % i)
        io.open(hp, 'w', encoding='utf8').write(PAGE % (html.escape(tr['title']) + ' · terminal', body))
        png = os.path.join(d, '%04d.png' % i)
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--window-size=1920,1080',
                        '--force-device-scale-factor=1', '--screenshot=' + png, 'file:///' + hp.replace(chr(92), '/')], capture_output=True, timeout=120)
        lst.append([png, dur])
    cl = os.path.join(d, 'list.txt')
    with io.open(cl, 'w', encoding='utf8') as f:
        for png, dur in lst:
            f.write("file '%s'\nduration %.3f\n" % (png.replace(chr(92), '/'), dur))
        f.write("file '%s'\n" % lst[-1][0].replace(chr(92), '/'))
    out = os.path.join(ROOT, 'videos', 'term-%s.mp4' % name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', cl, '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-crf', '20', '-an', out], check=True)
    print('wrote', out, len(lst), 'frames', round(sum(x[1] for x in lst), 1), 's')


if __name__ == '__main__':
    names = sys.argv[1:] or [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(HERE, 'term', '*.json')))]
    for n in names:
        build(n)
