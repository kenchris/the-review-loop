# Act IV. In practice

### 47
type: section
num: V
headline: In practice
sub: Four levels. Stop when it is enough.

### 48
type: fourup
tag: Act V · In practice
headline: Each level adds *one thing*
items:
- 01 | Ask for a review | One command, no setup.
- 02 | Tell it about your repo | Two minutes, once.
- 03 | Make "reviewed" a rule | For teams.
- 04 | Learn from outside review | Optional, pays off after a few rounds.

### 49
type: code
tag: Act V · Level 1
headline: Ask for a review
code: |
  /pre-pr-review
  /pre-pr-review 123
  /pre-pr-review main..my-branch
  /pre-pr-review multipass
caption: The current branch, a pull request, a range, or three readers and a vote. Fix what it finds and run it again.
source: These are typed to the agent (Claude Code, or VS Code), not to a shell.

### 50
type: code
tag: Act V · Level 1
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

### 51
type: code
tag: Act V · Level 2
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

### 52
type: code
tag: Act V · Level 2
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

### 53
type: video
tag: Recorded run
video: term-init.mp4
headline: Level 2 in *ten seconds*
caption: init creates REVIEW.md, REVIEW.sweeps, REVIEW.gate and reviews/. doctor checks the install.
machine: Windows 11, Git Bash. The output is real; the typing is replayed. Neon Smash, github.com/kenchris/soma-breakout

### 54
type: video
tag: Recorded run
video: vscode-tasks.mp4
headline: The same checks *inside VS Code*
caption: Terminal, Run Task, review-loop: sweeps. The wait for the terminal is cut. The hits are added as warnings on the lines, in the Problems panel and in the editor.
machine: VS Code on Windows 11, a clean profile, Neon Smash. Recorded live: the task output and the warnings are real.

### 55
type: video
tag: Recorded run
video: vscode-copilot.mp4
headline: /pre-pr-review in *Copilot chat*
caption: Agent mode in VS Code, on the last commit of Neon Smash. The report: no Important or Nit findings, and it says it could not run the tests.
machine: VS Code on Windows 11, recorded live. Typing 2 times and the agent's work 6 times faster, still stretches cut. /pre-pr-review HEAD~1..HEAD, a ten-line change.

### 56
type: statement
tag: Act V · Level 2
headline: Not every project wants this yet. *One or two developers can try it first.*
sub: Keep REVIEW.md, the sweeps and the reports in a separate private repository. The skills are installed per developer, so the project itself does not change.
source: review-loop reads its settings from a file outside the repository when REVIEW_LOOP_CONFIG names one.

### 57
type: diagram
tag: Act V · Level 2
headline: The project stays *as it is*
name: d-private
source: Our idea: a review-loop-private repository with one folder per project.

### 58
type: code
tag: Act V · Level 2
headline: One file says *where everything is*
code: |
  # review-loop-private/neon-smash/config.env
  REVIEW_FILE=$HOME/review-loop-private/neon-smash/REVIEW.md
  REVIEW_SWEEPS=$HOME/review-loop-private/neon-smash/REVIEW.sweeps
  REVIEWS_DIR=$HOME/review-loop-private/neon-smash/reviews
  EVALS_DIR=$HOME/review-loop-private/neon-smash/evals
caption: The reviewer reads REVIEW.md from there, the sweeps run from there, the reports and eval cases are kept there.
source: review-loop help, Configuration.

### 59
type: code
tag: Act V · Level 2
headline: Same commands, *nothing added to the project*
code: |
  $ export REVIEW_LOOP_CONFIG=~/review-loop-private/neon-smash/config.env
  $ cd neon-smash
  $ review-loop doctor
  ok       REVIEW.md (~/review-loop-private/neon-smash/REVIEW.md)
  ok       REVIEW.sweeps (optional)
  8 ok, 0 missing

  $ review-loop sweeps HEAD~7 HEAD
  [timer-in-loop] a timer: is it cleared when the game is reset or paused?
    js/secretCode.js:63:   for (let i = 0; i < ticks; i++) setTimeout(...)

  $ git status --short
  $
caption: A sweep from the private file fires. The project has no new files and nothing to commit.
source: Run on Neon Smash, HEAD~7 to HEAD, with the private files in a separate folder. Output shortened, paths shortened.

### 60
type: compare
tag: Act V · Level 2
headline: What a *private* setup gives, and what it does not
left_title: Works the same
left:
- /pre-pr-review, depth and sweeps
- Reports, scores and eval cases
- /retro on the outside comments you get
left_color: cyan
right_title: Does not, until it moves in
right:
- CI and the gate cannot see files that are not in the repository
- Teammates review with their own settings
- Nothing is shared yet
right_color: amber
source: Our reading of the configuration. Not tested in CI.

### 61
type: statement
tag: Act V · Level 2
headline: Moving in later is *a copy.*
sub: When the team says yes, copy the files to the project root and delete the config file. The root is the default place for all of them.
source: review-loop help: the defaults are REVIEW.md, REVIEW.sweeps, reviews/ and evals/ at the repository root.

### 62
type: code
tag: Act V · Level 3
headline: Make "reviewed" a rule
code: |
  /pre-pr-review multipass my-branch
      -> reviews/feature-limits-b23e6f49.md
         Open: 0

  review-loop gate main HEAD
  review gate: all 1 commit(s) covered by reports
caption: Commit the report. Check before a hand-over or merge.
source: Run on the example change made for this talk. The report is written by the agent, here by hand.

### 63
type: statement
tag: Act V · Level 3
headline: In CI the scripts run. *The skills do not.*
sub: Sweep hits appear as warnings on the changed lines of a pull request. The gate can be a required check.
source: docs/ci.md. The sample workflow is a sketch, not yet run on GitHub.

### 64
type: statement
tag: Act V · In practice
headline: Plain SKILL.md files. They work where an agent *loads skills.*
sub: Claude Code, VS Code (Copilot agent mode and the Claude Code extension), other agents that read a skills folder. The scripts need only bash and git.
source: README, VS Code.
