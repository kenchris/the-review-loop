#!/usr/bin/env python
"""Shortens long stretches where the screen does not change (waiting for the model) in a recording.
Usage: python trim-freezes.py in.mp4 out.mp4 [max_still_seconds=10]
Every still stretch longer than max_still_seconds is cut down to max_still_seconds; nothing else is touched.
The output is 1080p, 30 fps, H.264, no audio."""
import re, subprocess, sys

src, dst = sys.argv[1], sys.argv[2]
keep = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0

def run(args):
    return subprocess.run(args, capture_output=True, text=True)

dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', src]).stdout.strip())
fd = run(['ffmpeg', '-v', 'info', '-i', src, '-vf', 'freezedetect=n=-55dB:d=%s' % (keep + 1), '-an', '-f', 'null', '-']).stderr
starts = [float(x) for x in re.findall(r'freeze_start: ([\d.]+)', fd)]
ends = [float(x) for x in re.findall(r'freeze_end: ([\d.]+)', fd)]
if len(ends) < len(starts):
    ends.append(dur)
segs, pos = [], 0.0
for s, e in zip(starts, ends):
    cut_from, cut_to = s + keep, e
    if cut_to - cut_from > 0.5:
        segs.append((pos, cut_from))
        pos = cut_to
segs.append((pos, dur))
print('still stretches:', list(zip(starts, ends)))
print('kept segments:', segs)
parts = ''.join('[0:v]trim=start=%.3f:end=%.3f,setpts=PTS-STARTPTS[v%d];' % (a, b, i) for i, (a, b) in enumerate(segs))
cat = ''.join('[v%d]' % i for i in range(len(segs))) + 'concat=n=%d:v=1:a=0,scale=1920:1080:flags=lanczos,fps=30[out]' % len(segs)
r = run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-filter_complex', parts + cat, '-map', '[out]', '-c:v', 'libx264', '-crf', '20',
         '-preset', 'medium', '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart', dst])
print(r.stderr or 'ok')
