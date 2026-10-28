# Act II. The loop

### 23
type: section
num: III
headline: The loop
sub: What one review is made of, and what it costs.

### 24
type: diagram
tag: Act III · The loop
headline: Five parts, one *loop*
name: d13-loop

### 25
type: statement
tag: Act III · The loop
headline: A good reviewer reads *whole functions,* not diff lines.
sub: The callers and siblings needed to answer a question. The report says what was read in full and what was only skimmed.

### 26
type: fourup
tag: Act III · The loop
headline: Nineteen *lenses.* One question each.
items:
- Untrusted input | Missing, null, the wrong type, huge, negative, NaN?
- Error paths | Can it report success after the write failed?
- State | Every writer of a flag, and every reset of it.
- Claims | A comment says "never". Is that true for every caller?
source: skills/pre-pr-review/SKILL.md, section 3. Others: limits, cost, routing, platform, tests, concurrency, UI, dead code, other doors to the same resource.

### 27
type: code
tag: Act III · The loop
headline: A small change, three problems
lang: js
code: |
  function handle(body, settings) {
    const req = JSON.parse(body);
    const n = parseInt(req.limit);
    const items = req.tags.map((t) => t.trim());
    settings.lastLimit = n;
    return { ok: true, count: items.length, limit: n };
  }

  function showTitle(el, title) {
    el.innerHTML = title;
  }
caption: Twelve lines. Read it through the lenses and ask, for each line, what input breaks it.
source: A small example change made for this talk.

### 28
type: code
tag: Act III · The loop
headline: Verify: *write the failure,* then run it
code: |
  $ node probe.js
  {"limit":"1.5","tags":[" a "]} -> limit 1
  {"limit":"abc","tags":[]}      -> limit null
  {"limit":"5"}                  -> TypeError: reading 'map'
  null                           -> TypeError: reading 'limit'
caption: Every finding names the input that breaks it. What cannot be made concrete is dropped, or listed as "could not confirm".
source: Output of the probe on the example change, Node 22.

### 29
type: statement
tag: Act III · The loop
headline: Outside reviewers are cheap and sometimes wrong. *Yours should not be.*
sub: A finding without a concrete failure does not go in the report.

### 30
type: bignumber
tag: Act III · The loop
number: 37
unit: %
line: of the real problems found by *one cheap reader.*
side: **Our first baseline, code only, the cheapest model for every reader.** A small set of cases. It is the reason for the next slide, not a general result.
source: review-loop's own first baseline, in skills/pre-pr-review/references/multipass.md.
check: small sample. Say the number of cases, or leave it as "our first measurement".

### 31
type: diagram
tag: Act III · The loop
headline: Three readers, each with *one job,* then a vote
name: d20-multipass

### 32
type: compare
tag: Act III · The loop
headline: Pay for three readers only when it matters
left_title: One reader
left:
- Documentation and tests
- A small code change, away from any guard
- Costs one read of the diff
left_color: violet
right_title: Three readers and a vote
right:
- A larger change
- Always, for a path marked as a guard
- Costs about three reads
right_color: cyan
source: review-loop depth, skills/pre-pr-review/scripts/review-depth.sh. Default limit: 60 changed code lines.

### 33
type: code
tag: Act III · The loop
headline: It asks *before* you spend
code: |
  $ review-loop depth HEAD~1 HEAD
  depth: single
  why: small: 10 code lines (limit 60)

  $ review-loop depth HEAD~7 HEAD
  depth: multipass
  why: 393 code lines (a small change is up to 60)

  $ review-loop depth HEAD~20 HEAD
  depth: multipass
  why: 1731 code lines (a small change is up to 60)
caption: The last commit, the last seven and the last twenty of a real game.
source: Run on Neon Smash (github.com/kenchris/soma-breakout), October 2026.

### 34
type: statement
tag: Act III · The loop
headline: Three cycles at most. Then ask whether *the approach is wrong.*
sub: After the first pass, read only the new diff. Fix the class of a bug, not the line.

### 35
type: statement
tag: Act III · The loop
headline: What failure means *here* goes in one short file.
sub: REVIEW.md: what counts as a failure, which paths guard something, what to ignore, which classes were raised before. The reviewer reads it first.
