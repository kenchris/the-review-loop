#!/usr/bin/env python
"""Copies the web version (web/) into the public site repository's docs/ folder.
The site is a separate repository on purpose: it holds only the published pages and no history, so nothing
from this working repository (source documents, raw recordings, notes) can end up public.
Usage: python build/site.py [path to the site repository]     default: ../the-review-loop-site
It only copies. Look at `git status` in the site repository, commit there and push to publish."""
import os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), 'the-review-loop-site')
SRC = os.path.join(ROOT, 'web')
if not os.path.isdir(SRC):
    sys.exit('web/ is missing: run python make.py web first')
if not os.path.isdir(os.path.join(SITE, '.git')):
    sys.exit('not a git repository: %s' % SITE)
docs = os.path.join(SITE, 'docs')
if os.path.isdir(docs):
    shutil.rmtree(docs)
shutil.copytree(SRC, docs)
open(os.path.join(docs, '.nojekyll'), 'w').close()
print('copied web/ to', docs)
print(subprocess.run(['git', '-C', SITE, 'status', '--short'], capture_output=True, text=True).stdout or 'no changes')
