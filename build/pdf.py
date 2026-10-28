#!/usr/bin/env python
"""Builds deck.pdf: each slide is printed by Chrome as a 1920 x 1080 page (vector, searchable text), then merged.
Needs: pip install pypdf"""
import glob, os, subprocess, sys
from pypdf import PdfWriter, PdfReader
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, 'build')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
os.makedirs(os.path.join(B, 'pdf'), exist_ok=True)
def main():
    nums = sorted(int(os.path.basename(p)[:2]) for p in glob.glob(os.path.join(B, 'html', 'auto', '*.html')))
    only = [int(a) for a in sys.argv[1:] if a.isdigit()]
    for n in nums:
        out = os.path.join(B, 'pdf', '%02d.pdf' % n)
        if only and n not in only and os.path.exists(out):
            continue
        url = 'file:///' + os.path.join(B, 'html', 'auto', '%02d.html' % n).replace(chr(92), '/')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--virtual-time-budget=3000',
                        '--no-pdf-header-footer', '--print-to-pdf=' + out, url], capture_output=True, timeout=120)
    w = PdfWriter()
    for n in nums:
        r = PdfReader(os.path.join(B, 'pdf', '%02d.pdf' % n))
        w.add_page(r.pages[0])
    w.add_metadata({'/Title': 'The review loop', '/Author': 'Kenneth Rohde Christiansen'})
    out = os.path.join(ROOT, 'deck.pdf')
    w.write(out)
    print('wrote', out, len(nums), 'pages', round(os.path.getsize(out) / 1e6, 1), 'MB')
main()
