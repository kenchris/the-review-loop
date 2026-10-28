# Act VI. Limits and close

### 54
type: section
num: VI
headline: Limits
sub: What it does not do.

### 55
type: compare
tag: Act VI · Limits
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

### 56
type: statement
tag: Act VI · Limits
headline: Three readers cost about *three times* one. Say so before launching.
sub: The tool asks first for a large diff, suggests a model per reader, and the eval records the tokens each run used.

### 57
type: code
tag: Act VI · Close
headline: On Monday
code: |
  review-loop depth main HEAD
  review-loop sweeps main HEAD
  /pre-pr-review
caption: Free, free, and one reader. Fix what it finds. Stop here if that is enough.
source: Levels 1 and 2 of the README.

### 58
type: statement
tag: Act VI · Close
headline: Start at level 1. *Stop when it is enough.*
sub: github.com/kenchris/review-loop
