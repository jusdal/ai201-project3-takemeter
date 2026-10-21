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
flaired *App Issue*; a complaint is flaired *Discussion*), so the classifier
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

- *"Garden State AMC ScreenX"*: "It appears that the construction of the ScreenX theater in Garden State Plaza in NJ is complete, but they have a rope in front of the doors. Anyone have any idea when it's supposed to actually open?"
- *"Is AMC down for anyone else?"*: "Trying to entourage tickets for tonight, but regardless of time, theater, movie, or rating, I just keep getting the same 'Oops, an error has occurred; try again.' Was wondering if this was happening to anyone else currently or if my account is just bugged."

### `review`

**Definition:** The post gives the poster's verdict on a movie they have seen, focused on the film itself.

- *"La Bola Negra Is Stunningly Good"*: "Run, don't walk to see this movie. I was at the Burbank 16 and caught the Q&A with the directors…"
- *"Sooo....Street Fighter did not have to go that hard"*: "Beautifully shot! Lots of funny moments. Camp as hell with minimal cheese and just when I thought I knew how it was going to end....they pulled a fast one on me."

### `complaint`

**Definition:** The post criticizes AMC, a studio, or the theater experience, and isn't asking for help with a problem that's still happening.

- *"Ramayana"*: "i was actually excited to watch this... and was surprised that there is no screening in los angeles. what a bummer"
- *"Why are all the studios dropping great stuff in such a short period?"*: "There are 17 films out currently that I want to see… seriously, why do the studios drop so many good movies in such a short time frame?"

### `psa`

**Definition:** The post shares news or a fact about AMC, A-List, or upcoming releases, without giving a verdict on a movie or asking anything.

- *"Nolan's The Prestige 1/29"*: "Was unsure which theatres would be getting this. I am very excited! Edit: AMC has shared this on their IG page"
- *"Alex Gibney… is doing an AMA/Q&A in /r/movies today"*: "I organized an AMA/Q&A with Oscar-winning documentarian Alex Gibney… The AMA is live here now in r/movies for anyone interested in asking a question… He will be back after 2 PM ET today to answer questions."

### Hardest boundary: `question` vs. `complaint`

**Borderline post:** *"Musk - More Showtimes"*: "NYC based and spoiled with theater options, but somehow cannot find anymore Musk showings after work or on the weekend. Is it being phased out already? The Social Reckoning wasn't depressing enough for me that I'd like to sit through the 4 hours of this."

**Decision rule:** Apply these checks in order and stop at the first one that fits.

1. **`question`:** The post asks for information or advice that another member could give: a date, a policy, a recommendation, or "it's happening to me too." This includes "anyone else?" checks about a problem that is **still happening** (an app error, missing showtimes), even when the tone is angry. It does not include:
   - rhetorical questions or requests to agree with an opinion ("Is it just me or are the recliners getting worse?", "Why do studios release so much at once?")
   - "anyone else?" at the end of a story about something that's **already over** (a showing that got cancelled, a bad screening). Those go to step 4.
   - a question tacked onto a post that is mainly sharing news or a verdict. The question has to be the reason for the post.
2. **`review`:** The post gives a verdict on a movie the poster saw (a rating, a recommendation, or a clear "good/bad"). Problems with the screening don't change this. If there's no verdict on the film, go to step 4.
3. **`psa`:** The post shares news or a fact meant for other members to use (a release date, a policy change, an event), even if the poster sounds annoyed about it. **Test:** would another member do something differently after reading it (book a different showing, plan around an intermission, check a policy)? If yes, it's `psa`. If the post only describes the poster's own bad experience and gives readers nothing to act on, go to step 4.
4. **`complaint`:** Everything else that criticizes AMC, a studio, or the theater experience.

**Applied to the borderline post:** "Is it being phased out already?" can be answered with a fact, so *Musk - More Showtimes* is a `question`.

**A finding from labeling:** this was the hardest boundary I predicted in Milestone 2, but in practice `psa` vs. `complaint` turned out to be harder — it's the boundary behind the Doctor Strange crowd-reaction case below and the psa vs. complaint hard case in [The Dataset](#the-dataset).

### Second boundary to watch: `review` vs. `complaint`

*"The first five minutes of FJORD"* is about a movie the poster saw, but the whole post criticizes the studio logos before the film. Step 2 of the decision rule covers it: there's no verdict on the film, so it's a `complaint`.

### Boundaries `psa` adds

- **`psa` vs. `question`:** *"Has AMC discontinued those cardboard popcorn boxes?"* reports news (a worker said the change "came from the top") but ends with "Has anyone else heard about this?"
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

Mod and megathread posts, link or image-only posts, and posts that fit none of the four labels (for example the *"I think I have a problem"* concessions joke). I skipped 20 posts total: mod-sanctioned megathreads, image-only posts, personal stat logs ("A-List Report" style) with no verdict on any one movie, and jokes or asides with no question, verdict, news, or complaint in them.


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

| Label | Count | Share |
|---|---|---|
| `review` | 127 | 39.6% |
| `psa` | 86 | 26.8% |
| `question` | 75 | 23.4% |
| `complaint` | 33 | 10.3% |
| **Total** | **321** | **100%** |

`complaint`, at about 10% of the data, will only have around 5 posts in a
70/15/15 test split — small enough that its score will swing a lot between
seeds, the same caveat `criteria.md` already applies to `psa`.

**Three hard cases**

**1.**
> *The post:* "2nd summer in a row my AMC has had a broken air conditioner" — a long, detailed account (corporate emails, the AC failing again this year) that ends with "Has anyone else experienced this at their local AMC? Or other longtime maintenance issues that are ignored?"
>
> *Could have been:* `question` or `complaint`.
>
> *I chose, because:* I first labelled this `question`, reasoning the "anyone else" check was about a problem still happening. On reread I corrected it to `complaint` — the question is one line tacked onto several paragraphs of documented grievance, so it isn't the reason for the post. The "the question has to be the reason for the post" clause already existed (added for the "started early" case below); this is the case where I actually had to apply it to a heavily-venting post instead of a tidy one.

**2.**
> *The post:* "Returned to A-List" — "I just returned to A List after over a year and was pleasantly surprised to see 4dx was available and saw MK 2. For anybody on the fence, I think 4dx is a must for any 'fun' action movie."
>
> *Could have been:* `review` or `psa`.
>
> *I chose, because:* I first called this `review` since it's reacting to having seen a movie. But the verdict is on the 4DX format, not on Mortal Kombat 2 itself — and a format verdict isn't a movie verdict. Once I excluded that, step 3 fit instead: a reader could act on "4DX is available, try it for action movies." I corrected it to `psa`.

**3.**
> *The post:* "just a heads up for any women going to AMC Lincoln Square anytime soon" — a detailed account of a man sitting uncomfortably close in a nearly empty theater, ending with "I wanted to remind everyone to be vigilant!"
>
> *Could have been:* `psa` or `complaint`.
>
> *I chose, because:* I first labelled this `psa` because it opens with "heads up" like the other safety PSAs in the set. On a stricter reread, the problem is one person acting strange on one night, not something about the theater itself — unlike the mouse-at-Lincoln-Square or coyote-at-CityWalk posts, where the location is the actual, recurring source of the issue, so being alert there means something. This same man isn't reliably at AMC Lincoln Square; avoiding it wouldn't address anything. "Be vigilant" gives a reader nothing to actually act on. The post is overwhelmingly the poster's own unsettling experience, so I corrected it to `complaint`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

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

**Agreement rate:** ___ / 30 = ___%

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
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

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
