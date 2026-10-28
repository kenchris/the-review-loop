# Act IV. In practice

### 34
type: section
num: IV
headline: In practice
sub: Four levels. Stop when it is enough.

### 35
type: fourup
tag: Act IV · In practice
headline: Each level adds *one thing*
items:
- 01 | Ask for a review | One command, no setup.
- 02 | Tell it about your repo | Two minutes, once.
- 03 | Make "reviewed" a rule | For teams.
- 04 | Learn from outside review | Optional, pays off after a few rounds.

### 36
type: code
tag: Act IV · Level 1
headline: Ask for a review
code: |
  /pre-pr-review
  /pre-pr-review 123
  /pre-pr-review main..my-branch
  /pre-pr-review multipass
caption: The current branch, a pull request, a range, or three readers and a vote. Fix what it finds and run it again.
source: These are typed to the agent (Claude Code, or VS Code), not to a shell.

### 37
type: code
tag: Act IV · Level 1
headline: Install
code: |
  git clone https://github.com/kenchris/review-loop
  cd review-loop
  ./install.sh --link
  review-loop doctor

  # Windows
  .\install.cmd --for all --add-to-path
caption: Needs bash and git. On Windows, install.cmd finds the bash of Git for Windows.
source: README, Install.

### 38
type: code
tag: Act IV · Level 2
headline: Tell it about your repository
code: |
  $ review-loop init
  created  ./REVIEW.md
  created  ./REVIEW.sweeps
  created  ./REVIEW.gate
  ready    ./reviews/
  created  ./.review-loop.env

  $ review-loop doctor
  8 ok, 0 missing
caption: It never overwrites. Edit REVIEW.md a little: the reviewer reads it first.
source: Run on Neon Smash (github.com/kenchris/soma-breakout).

### 39
type: code
tag: Act IV · Level 2
headline: A REVIEW.md for a *small game*
code: |
  ## What a failure is here
  - Touch and keyboard doing different things
    for the same input.
  - A rule CLAUDE.md describes and the code
    does not do.

  ## Guards: read in full
  - js/secretCode.js  (once per game, never
    in a boss fight)
  - sw.js  (a stale cache serves an old game)
caption: Short on purpose. A reviewer that has to read a long file reads it badly.
source: REVIEW.md written for Neon Smash for this talk.

### 40
type: video
tag: Recorded run
video: term-init.mp4
headline: Level 2 in *ten seconds*
caption: init creates REVIEW.md, REVIEW.sweeps, REVIEW.gate and reviews/. doctor checks the install.
machine: Windows 11, Git Bash. The output is real; the typing is replayed. Neon Smash, github.com/kenchris/soma-breakout

### 41
type: video
tag: Recorded run
video: vscode-tasks.mp4
headline: The same checks *inside VS Code*
caption: Terminal, Run Task, review-loop: sweeps. The hits are added as warnings on the lines, in the Problems panel and in the editor.
machine: VS Code on Windows 11, a clean profile, Neon Smash. Recorded live: the task output and the warnings are real.

### 42
type: video
tag: Recorded run
video: vscode-copilot.mp4
headline: /pre-pr-review in *Copilot chat*
caption: Agent mode in VS Code, on the last commit of Neon Smash. The middle is sped up 12 times. The report: no Important or Nit findings, and it says it could not run the tests.
machine: VS Code on Windows 11. Recorded live, sped up in the middle. /pre-pr-review HEAD~1..HEAD, a ten-line change.

### 43
type: code
tag: Act IV · Level 3
headline: Make "reviewed" a rule
code: |
  /pre-pr-review multipass my-branch
      -> reviews/feature-limits-b23e6f49.md
         Open: 0

  review-loop gate main HEAD
  review gate: all 1 commit(s) covered by reports
caption: Commit the report. Check before a hand-over or merge.
source: Run on the example change made for this talk. The report is written by the agent, here by hand.

### 44
type: statement
tag: Act IV · Level 3
headline: In CI the scripts run. *The skills do not.*
sub: Sweep hits appear as warnings on the changed lines of a pull request. The gate can be a required check.
source: docs/ci.md. The sample workflow is a sketch, not yet run on GitHub.

### 45
type: statement
tag: Act IV · In practice
headline: Plain SKILL.md files. They work where an agent *loads skills.*
sub: Claude Code, VS Code (Copilot agent mode and the Claude Code extension), other agents that read a skills folder. The scripts need only bash and git.
source: README, VS Code.
