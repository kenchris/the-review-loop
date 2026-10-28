# Act VII. For managers

### 80
type: section
num: VII
headline: For managers
sub: What to decide, what to measure, how to start.

### 81
type: statement
tag: Act VII · For managers
headline: The question is not *"did a human read it?"* It is what could go wrong, and which check should catch it.
sub: The post calls reading by a person an imprecise proxy for that question.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 82
type: compare
tag: Act VII · For managers
headline: Who does what
left_title: Machines read
left:
- Routine mistakes in a diff
- Mechanical patterns, as sweeps
- Whether the tests ran and passed
left_color: cyan
right_title: People keep
right:
- Whether to build it at all
- Risky code: billing, the updater, CI workflows
- Architecture
- Owning the outcome
right_color: amber
source: The split is from Osmani, Lunt and Wang, 15 October 2026.

### 83
type: statement
tag: Act VII · For managers
headline: Whoever prompted the change is on the hook for it. *An agent's approval never counts as a person's.*
sub: The gate checks that a review was written. It never replaces the person who signs off.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 84
type: table
tag: Act VII · For managers
headline: What to *measure*
items:
- Measure | Where it comes from
- Human comments, and the time a PR waits on a person | Your tracker. review-loop does not measure it
- Recall and noise of the review | `review-loop eval report`
- Outside findings per round: the number should fall | `review-loop score show`
- Reverts and incidents: the guardrail | Your data. Turn each into an eval case
source: The measures are from Osmani, Lunt and Wang, 15 October 2026. The right column is review-loop's README.

### 85
type: statement
tag: Act VII · For managers
headline: The cost argument is *human time,* not tokens.
sub: A senior engineer pulled out of deep work to catch a routine mistake costs far more than an automated review. The post gives no dollar or token figures, and neither does this talk. review-loop records the tokens each run used, so you can measure your own.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 86
type: timeline
tag: Act VII · For managers
headline: A way to *roll it out*
items:
- Week 1 | One repository, or one or two developers with the files kept privately. Levels 1 and 2.
- Weeks 2 to 4 | Tune REVIEW.md as reviewers disagree with it.
- Then | Level 3: the gate, for the paths that guard something.
- After a few rounds | Level 4: learn from outside review.
source: The post: start with one repository, tune REVIEW.md for a few weeks, then widen. The mapping to levels is ours.

### 87
type: statement
tag: Act VII · For managers
headline: Start strict, *loosen with evidence.*
sub: In review-loop a guard path always gets three readers. Automatic risk tiers from the paths a change touches are planned, not built.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 88
type: fourup
tag: Act VII · For managers
headline: Four questions for your team
items:
- Ownership | Who owns a change an agent wrote?
- Guards | Which paths always need a person?
- Measures | What would make us tighten review?
- Memory | Where do review findings go after the round?
