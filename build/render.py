#!/usr/bin/env python
"""Renders build/html/auto/NN.html: art PNG (text hidden) and meta JSON (text geometry).
Usage: python render.py            (all)   |   python render.py 5 7   (some)   |   --full to also render a full preview (text visible)"""
import glob, io, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, 'build')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
os.makedirs(os.path.join(B, 'art'), exist_ok=True); os.makedirs(os.path.join(B, 'meta'), exist_ok=True); os.makedirs(os.path.join(B, 'full'), exist_ok=True)

def url(n, q):
    return 'file:///' + os.path.join(B, 'html', 'auto', '%02d.html' % n).replace(chr(92), '/') + q

def run(args):
    return subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run'] + args, capture_output=True, timeout=120)

def main():
    full = '--full' in sys.argv
    nums = [int(a) for a in sys.argv[1:] if a.isdigit()]
    if not nums:
        nums = sorted(int(os.path.basename(p)[:2]) for p in glob.glob(os.path.join(B, 'html', 'auto', '*.html')))
    for n in nums:
        r = run(['--window-size=1920,1080', '--virtual-time-budget=3000', '--dump-dom', url(n, '?meta=1')])
        m = re.search(r'<script id="meta" type="application/json">(.*?)</script>', r.stdout.decode('utf8', 'replace'), re.S)
        meta = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')) if m else []
        io.open(os.path.join(B, 'meta', '%02d.json' % n), 'w', encoding='utf8').write(json.dumps(meta, ensure_ascii=False))
        run(['--window-size=1920,1080', '--force-device-scale-factor=2', '--virtual-time-budget=3000',
             '--screenshot=' + os.path.join(B, 'art', '%02d.png' % n), url(n, '?art=1')])
        if full:
            run(['--window-size=1920,1080', '--force-device-scale-factor=1', '--virtual-time-budget=3000',
                 '--screenshot=' + os.path.join(B, 'full', '%02d.png' % n), url(n, '')])
        print('rendered', n, len(meta), 'text boxes')
main()
