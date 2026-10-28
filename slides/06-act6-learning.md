# Act V. Learning

### 65
type: section
num: VI
headline: Learning
sub: Every outside comment is a check you did not have.

### 66
type: statement
tag: Act VI · Learning
headline: If a bot reviews every push, *every push can bring new findings.*
sub: Copilot's review, CI and linters comment after you push. You fix, you push, and the next round finds something else. It starts to feel like a loop with no end. This part is for repositories where that is switched on.
source: Our experience. A real round: slide 7.

### 67
type: diagram
tag: Act VI · Learning
headline: From a review thread to *the next review*
name: d42-ledger
source: Every outside finding is a check you did not have. Learn from it, and the next push has fewer.

### 68
type: diagram
tag: Act VI · Learning
headline: The goal: *fewer findings after each push*
name: d-falling
source: An illustration of the aim. The number to watch is outside-new in review-loop score show.

### 69
type: code
tag: Act VI · Learning
headline: Level 4: *three* commands
code: |
  review-loop threads sync --repo owner/name

  /triage

  /retro round 26
caption: Download the open threads. The agent proposes a verdict for each, and you confirm once. Then it asks what would have caught them. By hand: threads worksheet and threads verdict.
source: docs/learning-from-reviews.md. Needs node 18 and a token that can read the pull requests.

### 70
type: statement
tag: Act VI · Learning
headline: Deciding every thread by hand is *the part people skip.*
sub: /triage reads each undecided thread against the code, proposes a verdict with the evidence, and records the ones you confirm in one call. Nothing is posted to GitHub and no code changes.
source: skills/triage/SKILL.md in review-loop.

### 71
type: screenshot
tag: Act VI · Learning
headline: /triage on *a real round*
image: triage-real-run.png
caption: 40 undecided threads on five pull requests, more than the skill reads in one go. So it split them by pull request, started three read-only readers and said it would check their proposals before showing anything.
callouts:
- The skill's own limit: over about 25 threads it reads in shares.
- Three readers, one share each. They edit nothing.
- Nothing is recorded until I confirm.
source: Claude Code, on a work project. The three readers had run for 51 seconds when this was taken.

### 72
type: screenshot
tag: Act VI · Learning
headline: Then it *checks the readers*
image: triage-real-run-2.png
caption: The first reader came back after 56 seconds. The agent did not pass its answer on. It listed where the reader was thin and what it would check itself first.
callouts:
- Three threads rejected on thin grounds. It will read the code before they go in the table.
- One verdict is mixed: only partly fixed.
- The reader skipped the headers and the PR text.
source: The same run, a little later. Claude Code, on a work project.

### 73
type: code
tag: Act VI · Learning
headline: What /triage *puts in front of you*
code: |
  id       where                  who      proposal  evidence
  a1b2c3d  js/secretCode.js:196   copilot  rejected  added once, at start-up
  e4f5a6b  js/assist.js:38        copilot  rejected  parse is in a try, value clamped

  Apply all, or tell me which ids to change.

  review-loop threads verdict --batch decisions.tsv
caption: One table, grouped by proposal, each with a line of evidence you can check. All or nothing when it records.
source: An example built from two sweep hits earlier in this talk, not real threads. The two runs before this slide were real.

### 74
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

### 75
type: diagram
tag: Act VI · Learning
headline: The cheapest change that *would have caught it*
name: d45-ladder

### 76
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

### 77
type: statement
tag: Act VI · Learning
headline: Measure the reviewer too. *Recall and noise.* Both.
sub: Recall: of the real problems, how many it reported. Noise: of what it reported, how much was wrong. Raising recall is easy. Noise is what it costs the author.
source: skills/review-eval/SKILL.md.

### 78
type: statement
tag: Act VI · Learning
headline: A rejected comment keeps *your reason.* It is not fixed twice.
sub: And a change to the lenses is kept only if the eval says it helped.

### 79
type: statement
tag: Act VI · Learning
headline: It pays off after a few rounds. *With one or two comments there is nothing to learn from yet.*
sub: Start with review-loop threads sync.
