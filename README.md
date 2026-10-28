# The review loop

A talk about review-loop (github.com/kenchris/review-loop): why it exists and how to use it. About 30 minutes (slides 1 to 58), then a hands-on part (59 to 63).

Built with the same pipeline as the web-after-the-ai-revolution talk. Text is in `slides/*.md`, drawings in `build/diagrams/*.html`.

    python make.py                 everything: slides, images, deck.pptx, deck.pdf, web/
    python make.py render 5 7      rebuild just slides 5 and 7
    python make.py preview 5 7     previews only, in build/full

Needs Python 3, Google Chrome, `pip install python-pptx pypdf pillow`.

Slides with a `check:` line still have a fact to confirm (slides 9, 10, 19, 50).

## Where the examples come from

- A real game, github.com/kenchris/soma-breakout: `review-loop depth`, `sweeps` and `init` were run on it (slides 22, 27, 28, 36, 37). The REVIEW.md on slide 37 was written for this talk.
- A small example change with three seeded bugs (slides 16, 17, 30, 38). The probe output and the gate output are real; the review report was written by hand in the skill's format.
