# Act VI. Limits and close

### 83
type: section
num: VIII
headline: Limits
sub: What it does not do.

### 84
type: compare
tag: Act VIII · Limits
headline: A small, generic version of some of these pieces
left_title: It does
left:
- Lenses, sweeps and verification
- Several readers and a vote
- A report, a gate and a score
- Retro and eval
left_color: cyan
right_title: It does not
right:
- Merge queues and staged rollout
- Feature flags
- Risk-tiered approval (planned)
- Explainers for modules (planned)
right_color: amber
source: README, Background, and PLAN.md.

### 85
type: statement
tag: Act VIII · Limits
headline: Three readers cost about *three times* one. Say so before launching.
sub: The tool asks first for a large diff, suggests a model per reader, and the eval records the tokens each run used.

### 86
type: code
tag: Act VIII · Close
headline: On Monday
code: |
  review-loop depth main HEAD
  review-loop sweeps main HEAD
  /pre-pr-review
caption: Free, free, and one reader. Fix what it finds. Stop here if that is enough.
source: Levels 1 and 2 of the README.

### 87
type: statement
tag: Act VIII · Close
headline: Start at level 1. *Stop when it is enough.*
sub: github.com/kenchris/review-loop

### 88
type: diagram
tag: Act VIII · Close
headline: *Read more,* and try it
name: d-links
