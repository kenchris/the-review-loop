# Act III. Checks that run

### 36
type: section
num: IV
headline: Checks that run
sub: Attention is expensive. A search is free.

### 37
type: statement
tag: Act IV · Checks that run
headline: If a search can find the pattern, *do not ask a reader to remember it.*
sub: A line in a prompt costs attention on every review. A sweep costs a second and no model.

### 38
type: code
tag: Act IV · Checks that run
headline: Sweeps: *the added lines,* run through search rules
code: |
  $ review-loop sweeps HEAD~20 HEAD
  [json-parse] throws on bad input: is the parsed
    shape checked before use?
    js/assist.js:38:  JSON.parse(localStorage.getItem(...))
  [new-listener] is there a matching removal?
    js/secretCode.js:191:  document.addEventListener(...)
  diff-sweeps: 15 question(s) for the author (warn-only)
caption: No model, no cost. Each hit is a question.
source: Run on Neon Smash (github.com/kenchris/soma-breakout), last 20 commits, output shortened.

### 39
type: statement
tag: Act IV · Checks that run
headline: A hit is *a question,* not a finding.
sub: Both of these are fine. The parse sits in a try and clamps the value. The listeners are added once, in a page that lives as long as the game. Answering takes a second.
source: js/assist.js and js/secretCode.js in Neon Smash.

### 40
type: video
tag: Recorded run
video: term-depth-sweeps.mp4
headline: Depth and sweeps on *a real game*
caption: Last commit: one reader. Last seven: three. Then the added lines run through the sweeps: two questions, no model.
machine: Windows 11, Git Bash. The output is real; the typing is replayed. Neon Smash, github.com/kenchris/soma-breakout

### 41
type: code
tag: Act IV · Checks that run
headline: Your own sweep is *one line*
code: |
  unchecked-parseint ## *.js ## parseInt\([^,)]*\) ## no radix, no NaN check:
    what do "abc" and "1.5" give?
caption: name ## which files ## regex ## why. It goes in REVIEW.sweeps at the root of the repository.
source: The format of REVIEW.sweeps.

### 42
type: code
tag: Act IV · Checks that run
headline: The gate: *"reviewed"* becomes a rule
code: |
  $ review-loop gate main HEAD
  FAIL: 1 commit(s) are in no review report
    with Open: 0, for example:
    b23e6f4 Add request handler
  STOP: run the multipass review and fix
    or explain every finding

  $ review-loop gate main HEAD~1
  review gate: all 1 commit(s) covered by reports
caption: A report in reviews/ with Open: 0 must cover every commit.
source: Run on the example change made for this talk.

### 43
type: statement
tag: Act IV · Checks that run
headline: The gate checks that a review *was written.* Not that it was good.
sub: It is a hand-over rule. Quality comes from the lenses, the readers, the verification and the eval.

### 44
type: video
tag: Recorded run
video: term-gate.mp4
headline: The gate fails, then *passes*
caption: No report: it stops. A report with Open: 0 that covers the commit: it passes.
machine: Windows 11, Git Bash. The output is real; the typing is replayed. The report was written by hand.
