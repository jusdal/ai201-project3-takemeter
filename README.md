# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

This classifier sorts posts from [r/AMCsAList](https://www.reddit.com/r/AMCsAList/),
a public subreddit for members of AMC Theatres' A-List subscription. Posts
aren't tied to one film or release — they cover reviews, theater and format
questions (IMAX, Dolby, ScreenX), app issues, and complaints about showtimes
and availability, with quality ranging from detailed firsthand reports to
one-line jokes. The subreddit's flairs aren't reliable labels (a joke post is
flaired _App Issue_; a complaint is flaired _Discussion_), so the classifier
sorts posts by why they were written, into three core labels —
`question`, `review`, and `complaint` — plus a stretch fourth label, `psa`,
for announcement-style posts (showtimes, policy changes, deals) that don't
fit the other three.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Community: r/AMCsAList. Labels sort posts by **why the post was written**.

### `question`

**Definition:** The post asks for information or advice another member could give.

- _"Garden State AMC ScreenX"_: "It appears that the construction of the ScreenX theater in Garden State Plaza in NJ is complete, but they have a rope in front of the doors. Anyone have any idea when it's supposed to actually open?"
- _"Is AMC down for anyone else?"_: "Trying to entourage tickets for tonight, but regardless of time, theater, movie, or rating, I just keep getting the same 'Oops, an error has occurred; try again.' Was wondering if this was happening to anyone else currently or if my account is just bugged."

### `review`

**Definition:** The post gives the poster's verdict on a movie they have seen, focused on the film itself.

- _"La Bola Negra Is Stunningly Good"_: "Run, don't walk to see this movie. I was at the Burbank 16 and caught the Q&A with the directors…"
- _"Sooo....Street Fighter did not have to go that hard"_: "Beautifully shot! Lots of funny moments. Camp as hell with minimal cheese and just when I thought I knew how it was going to end....they pulled a fast one on me."

### `complaint`

**Definition:** The post criticizes AMC, a studio, or the theater experience, and isn't asking for help with a problem that's still happening.

- _"Ramayana"_: "i was actually excited to watch this... and was surprised that there is no screening in los angeles. what a bummer"
- _"Why are all the studios dropping great stuff in such a short period?"_: "There are 17 films out currently that I want to see… seriously, why do the studios drop so many good movies in such a short time frame?"

### `psa`

**Definition:** The post shares news or a fact about AMC, A-List, or upcoming releases, without giving a verdict on a movie or asking anything.

- _"Nolan's The Prestige 1/29"_: "Was unsure which theatres would be getting this. I am very excited! Edit: AMC has shared this on their IG page"
- _"Alex Gibney… is doing an AMA/Q&A in /r/movies today"_: "I organized an AMA/Q&A with Oscar-winning documentarian Alex Gibney… The AMA is live here now in r/movies for anyone interested in asking a question… He will be back after 2 PM ET today to answer questions."

### Hardest boundary: `question` vs. `complaint`

**Borderline post:** _"Musk - More Showtimes"_: "NYC based and spoiled with theater options, but somehow cannot find anymore Musk showings after work or on the weekend. Is it being phased out already? The Social Reckoning wasn't depressing enough for me that I'd like to sit through the 4 hours of this."

**Decision rule:** Apply these checks in order and stop at the first one that fits.

1. **`question`:** The post asks for information or advice that another member could give: a date, a policy, a recommendation, or "it's happening to me too." This includes "anyone else?" checks about a problem that is **still happening** (an app error, missing showtimes), even when the tone is angry. It does not include:
   - rhetorical questions or requests to agree with an opinion ("Is it just me or are the recliners getting worse?", "Why do studios release so much at once?")
   - "anyone else?" at the end of a story about something that's **already over** (a showing that got cancelled, a bad screening). Those go to step 4.
   - a question tacked onto a post that is mainly sharing news or a verdict. The question has to be the reason for the post.
2. **`review`:** The post gives a verdict on a movie the poster saw (a rating, a recommendation, or a clear "good/bad"). Problems with the screening don't change this. If there's no verdict on the film, go to step 4.
3. **`psa`:** The post shares news or a fact meant for other members to use (a release date, a policy change, an event), even if the poster sounds annoyed about it. **Test:** would another member do something differently after reading it (book a different showing, plan around an intermission, check a policy)? If yes, it's `psa`. If the post only describes the poster's own bad experience and gives readers nothing to act on, go to step 4.
4. **`complaint`:** Everything else that criticizes AMC, a studio, or the theater experience.

**Applied to the borderline post:** "Is it being phased out already?" can be answered with a fact, so _Musk - More Showtimes_ is a `question`.

**A finding from labeling:** this was the hardest boundary I predicted in Milestone 2, but in practice `psa` vs. `complaint` turned out to be harder — it's the boundary behind the Doctor Strange crowd-reaction case below and the psa vs. complaint hard case in [The Dataset](#the-dataset).

### Second boundary to watch: `review` vs. `complaint`

_"The first five minutes of FJORD"_ is about a movie the poster saw, but the whole post criticizes the studio logos before the film. Step 2 of the decision rule covers it: there's no verdict on the film, so it's a `complaint`.

### Boundaries `psa` adds

- **`psa` vs. `question`:** _"Has AMC discontinued those cardboard popcorn boxes?"_ reports news (a worker said the change "came from the top") but ends with "Has anyone else heard about this?"
- **`psa` vs. `complaint`:** stress-test #8 ("the 4-reservation limit now counts tickets you already checked into… Found out the hard way") shares a fact, but in an annoyed tone.

Both are covered by the decision rule above: the popcorn-box post is a `question` (step 1), and stress-test #8 is a `psa` (step 3).

### Hard cases from the stress test

- **"Has anyone else noticed the A-List price going up every year? Feels like they're squeezing loyal members."** It could be `question` or `complaint`. I chose `question` because the price increase can be checked (step 1), even though the post is mostly venting. Risk: "anyone else noticed…" vents could thin out `complaint`. I'll watch the counts in Milestone 4. **Outcome:** it did run thin — `complaint` ended up the smallest label, and I had to hand-collect 10 more posts for it (see the `handpicked` note in The Dataset).
- **"Wildwood is a 9/10 for me… the sound was so loud it actually hurt, which knocked it down a point."** It could be `review` or `complaint`. I chose `review` because it gives a verdict on the film (9/10), and the screening problem doesn't change that. This case is why I reworded step 2 to look for a verdict instead of "the main point."

### Hard cases from cold labeling

- **"Heads-up: Musk has an intermission"** (`psa` or `review`): it shares a fact but ends with "It's also extremely good, go see it." I chose `review`, because step 2 (a verdict) comes before step 3.
- **"You Can See Everything started early"** (`psa` or `question`): it's a heads-up that ends with a spoiler question. I chose `psa`, because the question is an aside, not the reason for the post. This case is why step 1 now says the question has to be the reason for the post.
- **"I went to watch Verity twice"** (`review` or `question`): it ends with "Has anyone else watched Verity twice also?" I chose `review`, because the question is an aside to a verdict.
- **"Corrupted You Can See Everything"** (`complaint` or `question`): it tells the story of a showing that never played, then asks "Anyone else ever had this happen?" I chose `complaint`, because the problem is already over and the poster isn't really asking for help. This case is why step 1 now separates problems that are still happening from ones that are over.
- **"What's your favorite format?"** (`question` or none): it asks for opinions, not facts, so the original step 1 didn't cover it. I chose `question` and changed step 1 to say "information or advice."

### Hard cases from reviewing AI pre-labels

- **"PSA: Please don't tell fans when they react to be quiet…" (Doctor Strange)** (`psa` or `complaint`): it's angry at other moviegoers and built on a past grievance, but it tells readers to expect loud crowds Thursday through Saturday and to go Sunday morning if they want quiet. I chose `psa`, because readers could change which showing they book. This case is why step 3 now has the "would another member do something differently?" test.

### Posts left out of the dataset

Mod and megathread posts, link or image-only posts, and posts that fit none of the four labels (for example the _"I think I have a problem"_ concessions joke). I skipped 20 posts total: mod-sanctioned megathreads, image-only posts, personal stat logs ("A-List Report" style) with no verdict on any one movie, and jokes or asides with no question, verdict, news, or complaint in them.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** [r/AMCsAList](https://www.reddit.com/r/AMCsAList/).
I navigated to the subreddit's listing and search pages myself (`new`, `top`
this month, and searches for `flair:Discussion`, plus the keywords "PSA",
"heads up", and "FYI" — the keyword searches exist so announcement-style
posts don't get drowned out by the "new" feed's constant stream of
questions), saved each page's raw JSON output, and had the AI parse those
JSON files into `labels.csv` (title + selftext as the `text` column, `label`
and `note` left blank). Image/link-only posts, stickied posts, and
mod/megathread posts were filtered out during that parse. Posts span from
2022 to 2026 — a couple of the older ones (the Doctor Strange crowd-reaction
post, the Alamo Drafthouse post) are from 2022 and still matched the keyword
searches run now. Partway through labeling, `complaint` was running thin, so
I pulled a second, separate batch of fresh listings and handpicked 10 more
genuine complaints from it to round out that label (see the `handpicked` note
below).

**How I labelled them:** I wrote the taxonomy and its decision rule in
Milestone 2, before labeling, then cold-labelled the first 24 rows myself with
no AI help. Three of those cold-labelled posts ("started early," "Corrupted
You Can See Everything," and "What's your favorite format?") made me revise
the decision rule itself — see the hard cases under Label Taxonomy. (The
Musk-intermission post didn't change the rule; it just applied the existing
order, step 2 before step 3.) For the
remaining 307 rows, I had AI pre-label every row against that written decision
rule. The AI flagged 21 rows as `unsure`, and I reviewed each of those myself —
they produced most of my hard cases below. I also ran two full passes
specifically on `psa`, re-checking every `psa` row myself against the step-3
"would another member do something differently" test and fixing the ones that
failed it (2 flipped to `complaint` on reread). For the rest of the 307 — the
rows the AI didn't flag as `unsure` — I read its reasoning rather than
independently re-deriving each label myself, so I can't honestly claim a full
personal read of all 307; that's a real gap, not a full pass. 20 posts total
fit none of the four labels (mod-sanctioned megathreads, image-only posts,
personal stat logs with no verdict, jokes with no question/verdict/news/
complaint in them) and were removed rather than left in. The 10 rows noted
`handpicked` were chosen by hand from that second data pull specifically to
add more `complaint` examples, skipping anything already in the file.

**Counts per label:**

| Label       | Count   | Share    |
| ----------- | ------- | -------- |
| `review`    | 127     | 39.6%    |
| `psa`       | 86      | 26.8%    |
| `question`  | 75      | 23.4%    |
| `complaint` | 33      | 10.3%    |
| **Total**   | **321** | **100%** |

`complaint`, at about 10% of the data, will only have around 5 posts in a
70/15/15 test split — small enough that its score will swing a lot between
seeds, the same caveat `criteria.md` already applies to `psa`.

**Three hard cases**

**1.**

> _The post:_ "2nd summer in a row my AMC has had a broken air conditioner" — a long, detailed account (corporate emails, the AC failing again this year) that ends with "Has anyone else experienced this at their local AMC? Or other longtime maintenance issues that are ignored?"
>
> _Could have been:_ `question` or `complaint`.
>
> _I chose, because:_ I first labelled this `question`, reasoning the "anyone else" check was about a problem still happening. On reread I corrected it to `complaint` — the question is one line tacked onto several paragraphs of documented grievance, so it isn't the reason for the post. The "the question has to be the reason for the post" clause already existed (added for the "started early" case below); this is the case where I actually had to apply it to a heavily-venting post instead of a tidy one.

**2.**

> _The post:_ "Returned to A-List" — "I just returned to A List after over a year and was pleasantly surprised to see 4dx was available and saw MK 2. For anybody on the fence, I think 4dx is a must for any 'fun' action movie."
>
> _Could have been:_ `review` or `psa`.
>
> _I chose, because:_ I first called this `review` since it's reacting to having seen a movie. But the verdict is on the 4DX format, not on Mortal Kombat 2 itself — and a format verdict isn't a movie verdict. Once I excluded that, step 3 fit instead: a reader could act on "4DX is available, try it for action movies." I corrected it to `psa`.

**3.**

> _The post:_ "just a heads up for any women going to AMC Lincoln Square anytime soon" — a detailed account of a man sitting uncomfortably close in a nearly empty theater, ending with "I wanted to remind everyone to be vigilant!"
>
> _Could have been:_ `psa` or `complaint`.
>
> _I chose, because:_ I first labelled this `psa` because it opens with "heads up" like the other safety PSAs in the set. On a stricter reread, the problem is one person acting strange on one night, not something about the theater itself — unlike the mouse-at-Lincoln-Square or coyote-at-CityWalk posts, where the location is the actual, recurring source of the issue, so being alert there means something. This same man isn't reliably at AMC Lincoln Square; avoiding it wouldn't address anything. "Be vigilant" gives a reader nothing to actually act on. The post is overwhelmingly the poster's own unsettling experience, so I corrected it to `complaint`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`.

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. Trained on an Apple Silicon GPU (MPS), torch 2.14.1.

**Anything I changed from the defaults, and why:** Nothing — I kept the
notebook's defaults for this first run so the baseline reflects the stock
setup, not a tuning choice.

**Split sizes:** 321 posts, stratified 70/15/15 → train 224, val 48, test 49.
Per-label counts in the test split:

| Label       | Train | Val | Test |
| ----------- | ----- | --- | ---- |
| `question`  | 52    | 11  | 12   |
| `review`    | 89    | 19  | 19   |
| `psa`       | 60    | 13  | 13   |
| `complaint` | 23    | 5   | 5    |

`complaint` has only 5 examples in the test split — under the notebook's own
"thin" threshold of 8. With that few examples, its F1 can swing a lot between
seeds, which is exactly what The Dataset section already flagged as a risk
before training ever ran.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- _What I asked for:_ Pre-label the 307 empty rows in `labels.csv` against the
  taxonomy and decision rule I'd already written in Milestone 2, and flag
  anything genuinely close instead of guessing silently.
- _What came back:_ A label and a note for every row, applying the four-step
  rule in order, plus 21 rows flagged `unsure: X vs Y` and 18 rows flagged
  `SKIP` for fitting none of the four labels.
- _What I changed:_ Checking those `unsure` rows against the rule myself is
  where most of my corrections came from — 7 of the 8 total, including "2nd
  summer in a row my AMC has had a broken air conditioner" (question →
  complaint, because the question was one line tacked onto paragraphs of
  grievance) and "Returned to A-List" (review → psa, because the verdict was
  on the 4DX format, not the movie). I also removed the 18 `SKIP` rows rather
  than keep them.

**Moment 2**

- _What I asked for:_ A second pass, this time re-running every row labeled
  `psa` (87 of them, most already confirmed in the first pass) back through
  the step-3 "would another member do something differently" test, since
  that was the label most likely to have absorbed venting disguised as a
  heads-up.
- _What came back:_ 86 confirmed, 1 flipped — "just a heads up for any women
  going to AMC Lincoln Square" moved from `psa` to `complaint`, because "be
  vigilant" gives a reader nothing concrete to act on, unlike the mouse- and
  coyote-sighting posts that name a specific location worth being alert at.
- _What I changed:_ Accepted that flip — my 8th and last correction — and
  used it as a Dataset hard case. On a later feedback pass I caught that the
  AI's first write-up of that case contradicted itself — it said "no theater
  to avoid" in the same sentence the post names AMC Lincoln Square — and had
  it rewritten around the actual reasoning: the problem was one person on one
  night, not a theater-wide issue, so avoiding that location wouldn't do
  anything.

**Pre-labelling disclosure:** Yes. AI pre-labeled the 307 rows that weren’t cold-labeled, using my taxonomy and decision rule. I then read and checked every row myself and corrected 8 of them. The 24 cold rows were labeled by me with no AI help.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure          | Baseline | Trained | Difference |
| ---------------- | -------- | ------- | ---------- |
| Overall accuracy | 0.837    | 0.592   | -0.245     |
| Macro F1         | 0.806    | 0.425   | -0.382     |
| F1 — `complaint` | 0.667    | 0.000   | -0.667     |
| F1 — `psa`       | 0.870    | 0.593   | -0.277     |
| F1 — `question`  | 0.774    | 0.400   | -0.374     |
| F1 — `review`    | 0.914    | 0.706   | -0.208     |

Baseline is BART-MNLI zero-shot using bare label names. With my definitions from label_definitions.txt, it scored 0.571 accuracy and 0.362 macro F1, which is 0.266 lower. The likely cause is the "This post is {}." template, which turns each definition into a long, ungrammatical hypothesis with negations in it. I report the stronger run so the comparison with my trained model is fair.

**What I predicted before I looked:**

I predict the trained model's complaint F1 will beat the baseline's by at least 0.15. Zero-shot will confuse complaints with reviews, because both are negative and talk about the theater or the film. My definition separates them on whether the post is about the film itself, a distinction the trained model can learn from examples but BART-MNLI likely can't infer from one sentence.

**What the gap actually means:**

Fine-tuning added nothing. It made things worse. The trained model is below
the zero-shot baseline on every measure: 0.245 lower in accuracy, 0.382 lower
in macro F1, and lower on all four labels.

My prediction was wrong on both counts. Complaint F1 didn't improve: the
trained model scored 0.000 because it never predicted `complaint` once. The
baseline also didn't make the mistake I expected. It got 3 of 5 complaints
right, and the 2 it missed went to `question`, not `review`. Zero-shot never
mistook a complaint for a review.

The trained model's confusion matrix shows where it went wrong. It leans
heavily on `review`, my largest class (89 of 224 training posts). It sent 4 of
5 complaints, 5 of 12 questions and 5 of 13 PSAs to `review`. With only 23
complaint posts to learn from, it never learned to pick that label. It was
also unsure of itself: mean confidence was 0.47 on correct answers and 0.34 on
wrong ones. Its most confident third was 100% accurate and its least
confident third was 19%. That pattern looks like an undertrained model, not
one that learned the wrong rules. Three epochs on 224 posts may be too little
for DistilBERT, whose classification head starts from nothing. BART-MNLI is
much larger and has already been trained on entailment, which suits this task.

Limits on what this shows: it's one seed, and `complaint` has only 5 test
posts, so its 0.667 vs 0.000 rests on a handful of posts. The direction of the
gap is clear across every label, though. As trained, my model is worse than
running BART-MNLI with no training. The next things to try are more epochs and
class weighting for `complaint`, and the trained model should match or beat
0.837 before it's worth using.

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1. Overall accuracy | ≥ 0.75 | 0.592 | 0.531 | 0.551 | MISSED |
| 2. F1 on `question` / `review` / `complaint` | each ≥ 0.65 | 0.400 / 0.706 / 0.000 | 0.000 / 0.731 / 0.000 | 0.000 / 0.818 / 0.000 | MISSED |
| 3. F1 on `psa` | ≥ 0.50 | 0.593 | 0.483 | 0.486 | MISSED |
| 4. Label shares in `labels.csv` | none > 40%, none < 10% | 39.6% / 10.3% | 39.6% / 10.3% | 39.6% / 10.3% | MET |
| 5. Agreement with staff labels | ≥ 75% | 96.7% | 96.7% | 96.7% | MET |

Criteria 4 and 5 measure the dataset and my labelling, not the model, so they
are the same on every seed. Criterion 4's cells are the largest share
(`review`) and the smallest (`complaint`), and both pass by under 0.5 points.

### Spread across seeds

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.592 | 0.531 | 0.551 | 0.061 |
| Macro F1 | 0.425 | 0.303 | 0.326 | 0.121 |
| F1 — `question` | 0.400 | 0.000 | 0.000 | 0.400 |
| F1 — `review` | 0.706 | 0.731 | 0.818 | 0.112 |
| F1 — `psa` | 0.593 | 0.483 | 0.486 | 0.110 |
| F1 — `complaint` | 0.000 | 0.000 | 0.000 | 0.000 |

Accuracy moved 0.061 across seeds. Enough that a criterion landing within that band can't really be called either way.

The stability is misleading, though. In seeds 7 and 2024 the model predicts
only `review` and `psa`. Seed 42 is the only seed where it predicts `question`
at all (3 times), and it never predicts `complaint` on any seed. Accuracy stays in a narrow band because
the model fails the same way every time, not because it's reliable. Seed 42 was
also my best draw, so the single-seed numbers above (Baseline vs. Trained)
flatter the trained model.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42:

| true \ predicted | question | review | psa | complaint |
|---|---|---|---|---|
| **question** | 3 | 5 | 4 | 0 |
| **review** | 0 | 18 | 1 | 0 |
| **psa** | 0 | 5 | 8 | 0 |
| **complaint** | 0 | 4 | 1 | 0 |

**My biggest off-diagonal number, and what it means:**

5 real `question` posts were called `review` and none went the other way (tied
with 5 `psa` → `review`, 1 the other way), so the model barely learned
what makes a post a `question` (3 of 12 right) and falls back to `review`, my largest label, when
it's unsure.

<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| #   | Criterion | Target | Verdict | How I decided |
| --- | --------- | ------ | ------- | ------------- |
| 1   | Overall accuracy | ≥ 0.75 | MISSED | Below target on all three seeds (0.531–0.592). The best seed misses by 0.158. |
| 2   | F1 on `question`, `review`, `complaint` | each ≥ 0.65 | MISSED | Only `review` clears 0.65, on every seed. `complaint` is 0.000 on all three, and `question` is 0.000 on two. |
| 3   | F1 on `psa` | ≥ 0.50 | MISSED | 0.593 on seed 42, but 0.483 and 0.486 on the other two. It has to hold on all three. |
| 4   | Label shares | none > 40%, none < 10% | MET | `review` is 39.6% and `complaint` is 10.3%. Both pass, but narrowly. |
| 5   | Agreement with staff | ≥ 75% | MET | 29 of 30 (96.7%). |

**Diagnoses**

All three misses have the same cause: **the model is undertrained for this
much data.** It hasn't learned the smaller labels at all, so it guesses `review`
or `psa`. The evidence:

- **Training barely moved off chance.** A model guessing evenly among four
  labels has a loss of about 1.39. After 3 epochs, the last logged training loss was
  1.05, 1.05 and 0.98 across the seeds, and validation loss was still
  falling at the last epoch on every seed (seed 42: 1.24 → 1.12 → 1.06). Training
  stopped while the model was still improving.
- **The errors don't sit on one boundary.** They drift toward the big labels.
  Across the three seeds the model predicted `complaint` zero times and
  `question` only 3 times. Every true label leaks into `review` or `psa`, in
  one direction. A labelling problem would look different: confusion in both
  directions on one particular pair.
- **The labels themselves are learnable.** The zero-shot baseline, scored on
  the same seed-42 test posts, got 0.837 accuracy, with F1 of 0.774 on
  `question` and 0.667 on `complaint`. A model that has never seen my labels
  can separate them from the label names alone, so the distinctions are
  present in the text.
- **My agreement report points away from labelling.** I agreed with staff on
  29 of 30 posts, including posts chosen for being ambiguous. My one miss was
  reading in an argument the post didn't make, not applying a boundary two
  ways. That's under the staff taxonomy, not mine, so it's indirect evidence.
  But it's the only measure I have of my consistency, and it says I apply
  written rules consistently.

Per miss:

- **Criterion 1 (accuracy):** the cause is undertraining, as above. Accuracy
  sits around 0.55 because the model gets most reviews right (18–19 of 19)
  and about half the PSAs, and almost nothing else.
- **Criterion 2 (`question` / `review` / `complaint`):** `review` passes
  because it's the label the model falls back on. `complaint` fails for two
  reasons together. It has the fewest examples (23 in training, 5 in test),
  and the model never got far enough to learn a minority label. `question`
  is the more surprising miss, with 52 training posts. On seeds 7 and 2024
  most questions went to `psa` (7 of 12 and 11 of 12), not `review`. Both labels are often short,
  factual posts about AMC, so `question` vs. `psa` is the boundary I'd check
  in my own labels. But zero-shot gets `question` F1 0.774 on the same
  posts, which points to the model, not my labels.
- **Criterion 3 (`psa`):** `psa` is the model's second fallback label, so its
  recall is reasonable (0.54–0.69) and its precision is poor (0.38–0.57). It
  absorbs questions and complaints. It passed on seed 42 only. Partly that's a
  lucky draw, and partly it's because the seed-42 model sent its overflow to
  `review` instead.

None of the five criteria is broken. Each one named a number I could check,
so I've left them all as written. One reason in `criteria.md` turned out
wrong: criterion 3 expected `psa` to be my smallest label, but it was
`complaint`. That makes the target's reasoning weaker, not the criterion
unmeasurable, so it isn't grounds for a revision.

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** **29 / 30 = 96.7%**

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**

> _The post:_ "Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size."
>
> _Staff said / I said:_ `reaction` / `analysis`
>
> _My call, and why:_ Staff is right. I labelled it `analysis` because I read an argument into it: the wrong shoe size helped rather than hurt, or the writer had been wearing the wrong size all along. But the post never makes that claim. I supplied it. `analysis` needs the post itself to make an argument, with the fact doing work in it. This one states a fact and stops. What it actually does is report something the writer just noticed ("Just realised") about their own running, which is `reaction`. Rule 3 (recency doesn't outrank evidence) only applies when the fact is load-bearing, and here there's no stated argument for it to carry.
>
> _Which pile:_ (a) — the rule covered it and I applied it loosely. The definition says `analysis` *makes* an argument. I counted an argument the post only implied, so I was judging what the writer might have meant instead of what they wrote.

**What the pattern in my disagreements tells me:**

With one disagreement in 30 there's hardly a pattern, and that is the main
finding. I applied a taxonomy I didn't write the same way its authors did on
29 of 30 posts, including posts staff picked because they're ambiguous. That's
evidence I can apply written rules consistently, which makes it less likely my
own 321 labels are full of inconsistency.

The one miss shows the kind of mistake I make: reading in an argument the
writer implies but doesn't state. That matters for my own taxonomy, whose
decision rule has the same kind of judgement in it ("the question has to be
the reason for the post", "would another member do something differently?").
Where I applied those rules generously, labels could drift. The most likely
place is the `psa` vs. `complaint` boundary, which I already found hardest.

It doesn't explain my model's results, though. The trained model doesn't fail
on one boundary. It sends every label toward `review`, across all three seeds,
and the zero-shot baseline scores 0.837 on the same labels. A labelling
problem would show up as confusion on particular boundaries. Errors that all
drift toward the largest class point to a model problem: too little data and
training (23 complaint posts, 3 epochs), not inconsistent labels.

---

## The Improvement

**What I changed:** One training setting: `EPOCHS` from 3 to 10. Everything
else is unchanged: same `labels.csv`, same seeds (42, 7, 2024), learning rate
2e-5, batch size 16 and max length 128.

**Which diagnosis pointed at it:** Undertraining. Validation loss was still
falling at epoch 3 on every seed, training loss ended around 1.0 (chance is
about 1.39), and the model never predicted `complaint` and almost never
`question`. Zero-shot scoring 0.837 on the same labels, and 96.7% agreement
with staff, both point away from relabelling. So this is the one case where
the diagnosis points at training and not at the data.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1. Overall accuracy | ≥ 0.75 | 0.857 | 0.755 | 0.776 | MET |
| 2. F1 on `question` / `review` / `complaint` | each ≥ 0.65 | 0.889 / 0.947 / 0.000 | 0.640 / 0.872 / 0.000 | 0.741 / 0.900 / 0.000 | MISSED |
| 3. F1 on `psa` | ≥ 0.50 | 0.857 | 0.828 | 0.769 | MET |
| 4. Label shares in `labels.csv` | none > 40%, none < 10% | 39.6% / 10.3% | 39.6% / 10.3% | 39.6% / 10.3% | MET |
| 5. Agreement with staff labels | ≥ 75% | 96.7% | 96.7% | 96.7% | MET |

Spread across seeds, after:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.857 | 0.755 | 0.776 | 0.102 |
| Macro F1 | 0.673 | 0.585 | 0.602 | 0.089 |
| F1 — `question` | 0.889 | 0.640 | 0.741 | 0.249 |
| F1 — `review` | 0.947 | 0.872 | 0.900 | 0.076 |
| F1 — `psa` | 0.857 | 0.828 | 0.769 | 0.088 |
| F1 — `complaint` | 0.000 | 0.000 | 0.000 | 0.000 |

**Did it help, and how do I know:**

Yes, a lot, but not on the label that needed it most. Criteria 1 and 3 went
from MISSED to MET, so the run went from 2 of 5 to 4 of 5. Accuracy rose by
about 0.22–0.27 on every seed (seed 42: 0.592 → 0.857), and macro F1 rose by
about 0.25–0.28. On seed 42 the trained model now beats the zero-shot
baseline on accuracy (0.857 vs. 0.837), which it was 0.245 behind before.

The evidence that undertraining was the cause:

- **The collapse is gone.** Before, the model predicted `question` 3 times
  across all three seeds. Now it gets 8–12 of 12 questions right on every
  seed. `question` F1 went from 0.400 / 0.000 / 0.000 to 0.889 / 0.640 / 0.741.
- **Loss kept falling, with no sign of overfitting.** Validation loss dropped
  on every epoch on every seed (seed 42: 1.22 at epoch 1 → 0.51 at epoch 10)
  and was only levelling off by epoch 10. It never turned back up.
- **Confidence now means something.** Mean confidence on right answers rose
  from about 0.5 to 0.85 on every seed.

**What it didn't fix:** `complaint` is still 0.000 on every seed. The model
still never predicts it. The pattern of its misses has changed, though, and
the change is informative. Before, complaints went to `review` like
everything else. Now most go to `question` (2, 3 and 3 of 5), and no real
question was ever called `complaint`. That's my hardest boundary from Milestone 2,
`question` vs. `complaint`, showing up once the model is trained enough to
learn boundaries at all. With only 23 complaints in training, the model learns
the side of that boundary it has more examples of.

**The new spread:** accuracy now moves 0.102 across seeds, just over the
10-point line, where before it was 0.061. The notebook calls this a sign the
dataset is too small for a stable measure, and I agree. With 49 test posts,
each post is worth about 2 points of accuracy, so 0.102 is 5 posts. The spread
grew because the model now makes real distinctions, and which posts land in
each test split matters more. Criterion 1 passes on seed 7 by 0.005, less than
one post, so it's a pass I wouldn't lean on.

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**The gap between what I meant my labels to capture and what the model
learned:**

<!-- Two sentences. Your confusion matrix is the evidence. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
