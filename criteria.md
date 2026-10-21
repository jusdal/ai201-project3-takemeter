# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

Overall accuracy on the held-out test set is at least **0.75**.

**Why this target:** With four labels, random guessing gets about 25%, and
always guessing my biggest label (`question`) would probably get around 40%.
0.75 is well above both. It's high enough that I'd trust the model to sort a
feed, but within reach for a small model trained on about 140 posts.

---

## 2.

`question`, `review`, and `complaint` each have an F1 of at least **0.65** on
the test set.

**Why this target:** I set this a little below my 0.75 accuracy target, since
overall accuracy is roughly an average and some labels will score below it.
`question` vs. `complaint` is my hardest boundary, so I expect those two to
come in lowest. 0.65 is still clearly better than guessing.

---

## 3.

`psa` has an F1 of at least **0.50** on the test set.

**Why this target:** `psa` will probably be my smallest label, with only
about 3–4 posts in the test set, so each one changes its F1 a lot. I'm
setting a lower target here because there are so few examples to measure, not
because I expect less of the label.

---

## 4.

No label is more than **40%** of `labels.csv`, and no label is under **10%**.

**Why this target:** The notebook's 70% cap is too loose for four labels —
with four labels an even split is 25% each, so a label at 70% would mean the
other three are splitting the remaining 30% between them, which isn't a
four-way classifier anymore. **40%** lets one label lead by a wide margin
(`question` is the label most at risk, because my rule counts "anyone else?"
posts as questions) while still leaving the other three at least 20% each to
share. **10%** is the floor because, at ~200 posts, 10% is about 20 examples
— with a 70/15/15 split that's only 2–3 in the test set, which is already
what I sized my `psa` F1 target around in #3. Below that, there'd be too
little in either train or test to call the measurement meaningful.

---

## 5.

My labels agree with the staff labels on at least **75%** of posts.

**Why this target:** People labeling posts with clear definitions usually
agree on 70–85% of them. I expect most disagreements at the
`question`/`complaint` boundary, especially on "anyone else?" posts that are
really vents, so I aimed for the middle of that range rather than the top.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
