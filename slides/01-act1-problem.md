# Act I. The problem

### 4
type: section
num: I
headline: The problem
sub: Writing got cheap. Reading did not.

### 5
type: statement
tag: Act I · The problem
headline: A change you did not type is a change you have to *read.*
sub: And an agent produces them faster than anyone can read.

### 6
type: compare
tag: Act I · The problem
headline: Two moments to find out a change is wrong
left_title: After it goes out
left:
- A reviewer, a bot or a user finds it
- You fix it in another round
- The next change gets the same comment
left_color: amber
right_title: Before it goes out
right:
- The same checks run first
- It is fixed in the same round
- The class of bug gets a check
right_color: cyan

### 7
type: bignumber
tag: Act I · The problem
number: 8
unit: of 9
line: outside review comments on three pull requests were *right.*
side: **All eight were fixed. None of them changed the next review.** The fixes disappeared into the pull requests.
source: Our own: a real round on one of our projects, from the review-loop README. Copilot comments on three pull requests.

### 8
type: statement
tag: Act I · The problem
headline: Fixing a comment fixes *one line.* The next change gets the same comment.
sub: Nothing in the process remembers.

### 9
type: statement
tag: Act I · The problem
headline: Most of our time goes on *reading,* and how we read is almost never discussed.
sub: So it is never improved.
source: Tudor Girba and Simon Wardley, "Rewilding software engineering", chapter 1, 2025.
check: confirm the wording against chapter 1 before quoting it as a quote.

### 10
type: diagram
tag: Act I · The problem
headline: The post this talk keeps *coming back to*
name: d10-post
source: Osmani, Lunt and Wang, claude.dev, 15 October 2026.

### 11
type: statement
tag: Act I · The problem
headline: The Claude Code team reviews its agent-written code in *layers.*
sub: Verify before the pull request. An AI review on every pull request, its findings checked by other agents. A file that says what matters. Past incidents as the test set.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", claude.dev, 15 October 2026.

### 12
type: statement
tag: Act I · The problem
headline: Several of these points are *also our own conclusions,* from working on our own products.
sub: We hit the same problems: comments that taught the next review nothing, one reader finding only part of what outside reviewers found, three readers costing three times one. review-loop is what we built.
source: The numbers shown for review-loop are our own measurements, small and early.
check: say which products, and what you saw there.

### 13
type: statement
tag: Act I · The problem
headline: Not a step at the end. *A loop* that gets better each round.
sub: Check it yourself. Let others check it. Turn what they find into a check that runs.
