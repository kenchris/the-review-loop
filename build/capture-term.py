#!/usr/bin/env python
"""Runs the real commands and stores their output in build/term/*.json (a transcript: command, output, exit code).
Usage: python capture-term.py <soma-breakout clone> <demo repo>"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'term')
RL = 'C:/Users/kenne/Repo/review-loop/bin/review-loop'
soma, demo = sys.argv[1], sys.argv[2]

def run(cwd, cmd, shown=None):
    r = subprocess.run(['bash', '-c', cmd.replace('review-loop', RL, 1) if cmd.startswith('review-loop') else cmd],
                       cwd=cwd, capture_output=True, text=True, encoding='utf8')
    out = (r.stdout + r.stderr)
    out = re.sub(r'warning: in the working copy.*\n', '', out)
    out = out.replace(cwd.replace(chr(92), '/') + '/', './')
    return {'cmd': shown or cmd, 'out': out.rstrip('\n'), 'code': r.returncode}

def save(name, steps, title):
    json.dump({'title': title, 'steps': steps}, open(os.path.join(OUT, name + '.json'), 'w', encoding='utf8'), indent=1)

# 1. depth and sweeps on the game (main, so the numbers match the slides)
subprocess.run(['git', 'checkout', '-q', 'main'], cwd=soma)
save('depth-sweeps', [run(soma, c) for c in (
    'review-loop depth HEAD~1 HEAD', 'review-loop depth HEAD~7 HEAD', 'review-loop sweeps HEAD~7 HEAD')], 'soma-breakout')

# 2. the gate: fails without a report, passes with one
subprocess.run(['git', 'checkout', '-q', 'feature/limits'], cwd=demo)
rep = [f for f in os.listdir(os.path.join(demo, 'reviews')) if f.startswith('feature-limits')][0]
rp = os.path.join(demo, 'reviews', rep); hold = rp + '.hold'
shutil.move(rp, hold)
s1 = run(demo, 'review-loop gate main b23e6f49')
shutil.move(hold, rp)
s2 = run(demo, 'head -7 reviews/' + rep)
s3 = run(demo, 'review-loop gate main b23e6f49')
save('gate', [s1, s2, s3], 'example change')

# 3. init and doctor in a fresh copy of the game
tmp = os.path.join(os.path.dirname(os.path.abspath(soma)), 'soma-init')
shutil.rmtree(tmp, ignore_errors=True)
subprocess.run(['git', 'clone', '-q', soma, tmp])
subprocess.run(['git', 'checkout', '-q', 'main'], cwd=tmp)
save('init', [run(tmp, 'review-loop init'), run(tmp, 'review-loop doctor')], 'soma-breakout')
print('ok')
