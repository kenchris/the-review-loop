# Act V. Learning

### 65
type: section
num: VI
headline: Learning
sub: Every outside comment is a check you did not have.

### 66
type: diagram
tag: Act VI · Learning
headline: From a review thread to *the next review*
name: d42-ledger

### 67
type: code
tag: Act VI · Learning
headline: Level 4: four commands
code: |
  review-loop threads sync --repo owner/name
  review-loop threads worksheet
  review-loop threads verdict <id> fixed --commit <sha>

  /retro round 26
caption: Download the open threads. See what is undecided. Decide each one. Then ask the agent what would have caught them.
source: docs/learning-from-reviews.md. Needs node 18 and a token that can read the pull requests.

### 68
type: table
tag: Act VI · Learning
headline: A verdict is *your decision* about one thread
items:
- Verdict | Meaning
- fixed | Right, and fixed. Give the commit.
- rejected | Wrong. Say why: it is remembered.
- caught | My own review had already reported it.
- deferred | Real, but not now.
source: docs/learning-from-reviews.md. Also: missed, and new for undecided.

### 69
type: diagram
tag: Act VI · Learning
headline: The cheapest change that *would have caught it*
name: d45-ladder

### 70
type: fourup
tag: Act VI · Learning
headline: What /retro said about a real round
items:
- Three | The lens covered it, the reader skipped it.
- One | A one-line search would find it: a pointer cast with no family check.
- One | A deleted test file nobody had noticed.
- Result | A ranked list of changes, instead of nine fixes that teach nothing.
source: The Copilot round from slide 7: nine comments, eight right. The README does not break down the other three.
check: the README gives five of the eight causes. Do not claim a split of the rest.

### 71
type: statement
tag: Act VI · Learning
headline: Measure the reviewer too. *Recall and noise.* Both.
sub: Recall: of the real problems, how many it reported. Noise: of what it reported, how much was wrong. Raising recall is easy. Noise is what it costs the author.
source: skills/review-eval/SKILL.md.

### 72
type: statement
tag: Act VI · Learning
headline: A rejected comment keeps *your reason.* It is not fixed twice.
sub: And a change to the lenses is kept only if the eval says it helped.

### 73
type: statement
tag: Act VI · Learning
headline: It pays off after a few rounds. *With one or two comments there is nothing to learn from yet.*
sub: Start with review-loop threads sync.
