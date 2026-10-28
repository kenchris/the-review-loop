# Hands-on

### 59
type: section
num: VII
headline: Hands-on
sub: On your own branch. About 20 minutes.

### 60
type: fourup
tag: Hands-on
headline: Six steps
items:
- 01 | Install | review-loop doctor shows 8 ok.
- 02 | Ask | /pre-pr-review on a branch with changes.
- 03 | Compare | review-loop depth, then sweeps.
- 04 | Setup | review-loop init, edit REVIEW.md.
- 05 | Rule | Save a report, run the gate.
- 06 | Learn | Optional: threads sync, then /retro.

### 61
type: code
tag: Hands-on · Steps 1 to 3
headline: Install, ask, compare
code: |
  ./install.sh --link
  review-loop doctor

  /pre-pr-review

  review-loop depth main HEAD
  review-loop sweeps main HEAD
caption: Did the review find something the sweeps did not? Did the sweeps ask something the review answered?

### 62
type: code
tag: Hands-on · Steps 4 and 5
headline: Setup, then the rule
code: |
  review-loop init
  review-loop doctor

  /pre-pr-review multipass my-branch
  review-loop gate main HEAD
caption: Edit REVIEW.md first: three lines on what failure means in your project.

### 63
type: statement
tag: Hands-on · Step 6
headline: For those with *open pull requests* and review comments.
sub: review-loop threads sync --repo owner/name, then decide each thread. Then /retro, and read the list before you apply anything.
