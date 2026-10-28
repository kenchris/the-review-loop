# Act II. Why it matters

### 14
type: section
num: II
headline: Why it matters
sub: What one team found when agents wrote most of the code, and how review-loop answers it.

### 15
type: bignumber
tag: Act II · Why it matters
number: 30,000
line: changes *a day* landing in Anthropic's monorepo in September, up from about 2,500 in May.
side: **Claude writes about 90% of Claude Code's own code.** Claude Code has its own repository, and the post says it feels the same pressure.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", claude.dev, 15 October 2026. The 30,000 is for the monorepo, not for Claude Code's repository.

### 16
type: statement
tag: Act II · Why it matters
headline: When you ship this fast, line-by-line review is *incredibly difficult, if not impossible.*
sub: They did not drop review. They moved most of the reading to machines and kept people for what machines cannot decide.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 17
type: statement
tag: Act II · Why it matters
headline: The goal: *less human time per change,* and no more reverts than before.
sub: Reverts and incidents are the guardrail. Human approvals per pull request, human comments and the wait for a person are what they push down.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 18
type: bignumber
tag: Act II · Why it matters
number: 40
unit: %
line: drop in the share of merged pull requests that had to be *reverted,* while the number merged more than doubled.
side: **Claude Code repositories, June to September.** The post gives the direction and the share, not the counts.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 19
type: bignumber
tag: Act II · Why it matters
number: 54
unit: %
line: of internal pull requests got *substantive review comments,* up from 16%.
side: **At the launch of the research preview of their AI review.** The post does not say whether 54% is the current figure.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 20
type: table
tag: Act II · Why it matters
headline: What the post does, and *where it lives here*
items:
- The post | In review-loop
- Verify before the pull request, with a fresh reader | `/pre-pr-review`
- A REVIEW.md written by the code owners | `REVIEW.md`, created by `review-loop init`
- Parallel reviewers, a vote, findings tagged Important, Nit or Pre-existing | `multipass`: three readers, a vote, the same labels
- Every finding fixed, or resolved with a reason | `review-loop gate`: a report with Open: 0
source: Practices from Osmani, Lunt and Wang, 15 October 2026. The right column is review-loop's own README.

### 21
type: table
tag: Act II · Why it matters
headline: ...and *the rest* of the map
items:
- The post | In review-loop
- Fix recurring findings at the source | Sweeps in `REVIEW.sweeps`, and `/retro`
- Review has to converge | Three cycles, only the new diff, fix the class
- Past incidents as the reviewer's test set, noise measured | `/review-eval`: recall and noise
- Merge queue, feature flags, gradual release | Not covered. Risk tiers: planned
source: Practices from Osmani, Lunt and Wang, 15 October 2026. The right column is review-loop's own README.

### 22
type: table
tag: Act II · Why it matters
headline: Review has to *converge*
items:
- Internal pull requests | Before, then after
- Pass after one review-and-fix round | 65%, then 78%
- Need five or more rounds | 8.9%, then 1.5%
- Mean number of reviews to pass | 2.08, then 1.32
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026. Before and after the team's convergence work.

### 23
type: statement
tag: Act II · Why it matters
headline: One pull request went through *more than fifty rounds* of review and fixes overnight.
sub: A person dismisses a nit in seconds. An agent makes another commit and starts another round. review-loop stops at three cycles, reads only the new diff, and fixes the class of a bug, not the line.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026.

### 24
type: bignumber
tag: Act II · Why it matters
number: 59
unit: %
line: of what the reviewer kept flagging was *old code,* there since the first pass.
side: **review-loop marks it Pre-existing** and keeps it out of the author's count, so a round does not grow on code the change never touched.
source: Osmani, Lunt and Wang, "How the Claude Code team does code review", 15 October 2026. By git blame, on the pull requests the team studied.
