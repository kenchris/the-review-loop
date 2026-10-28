#!/usr/bin/env python
"""One command for the whole deck.

  python make.py                 build everything: slides -> images -> deck.pptx and deck.pdf
  python make.py pptx            only (re)build the PowerPoint from the existing images
  python make.py pdf             only (re)build the PDF
  python make.py web             only (re)build the web version in web/
  python make.py site            copy web/ into the public site repository (../the-review-loop-site/docs)
  python make.py render 5 7 13   rebuild and re-render only slides 5, 7 and 13, then pptx and pdf
  python make.py preview 5 7     rebuild only these slides and show full previews in build/full

Slide text lives in slides/*.md, diagrams in build/diagrams/*.html.
Needs Python 3, Google Chrome, and: pip install python-pptx pypdf
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, 'build')
def run(script, *args):
    r = subprocess.run([sys.executable, os.path.join(B, script)] + list(args))
    if r.returncode:
        sys.exit(r.returncode)
def main():
    a = sys.argv[1:]
    cmd = a[0] if a and not a[0].isdigit() else 'all'
    nums = [x for x in a if x.isdigit()]
    if cmd in ('all', 'render', 'preview'):
        run('build.py', *nums)
        run('render.py', *nums, '--full')
    if cmd in ('all', 'render', 'pptx'):
        run('assemble.py')
    if cmd in ('all', 'render', 'pdf'):
        run('pdf.py', *nums)
    if cmd in ('all', 'render', 'web', 'preview'):
        run('web.py')
    if cmd == 'site':
        run('site.py')
main()
