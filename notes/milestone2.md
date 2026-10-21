# Milestone 2: Label Taxonomy

Community: r/AMCsAList. Labels sort posts by **why the post was written**.

## Labels

### `question`
**Definition:** The post asks the community for specific information that another member could answer with a fact or their own experience.

- *"Garden State AMC ScreenX"*: "It appears that the construction of the ScreenX theater in Garden State Plaza in NJ is complete, but they have a rope in front of the doors. Anyone have any idea when it's supposed to actually open?"
- *"Is AMC down for anyone else?"*: "Trying to entourage tickets for tonight, but regardless of time, theater, movie, or rating, I just keep getting the same 'Oops, an error has occurred; try again.' Was wondering if this was happening to anyone else currently or if my account is just bugged."

### `review`
**Definition:** The post gives the poster's verdict on a movie they have seen, focused on the film itself.

- *"La Bola Negra Is Stunningly Good"*: "Run, don't walk to see this movie. I was at the Burbank 16 and caught the Q&A with the directors…"
- *"Sooo....Street Fighter did not have to go that hard"*: "Beautifully shot! Lots of funny moments. Camp as hell with minimal cheese and just when I thought I knew how it was going to end....they pulled a fast one on me."

### `complaint`
**Definition:** The post criticizes AMC, a studio, or the theater experience, and doesn't ask anything another member could answer.

- *"Ramayana"*: "i was actually excited to watch this... and was surprised that there is no screening in los angeles. what a bummer"
- *"Why are all the studios dropping great stuff in such a short period?"*: "There are 17 films out currently that I want to see… seriously, why do the studios drop so many good movies in such a short time frame?"

### `psa`
**Definition:** The post shares news or a fact about AMC, A-List, or upcoming releases, without giving a verdict on a movie or asking anything.

- *"Nolan's The Prestige 1/29"*: "Was unsure which theatres would be getting this. I am very excited! Edit: AMC has shared this on their IG page"
- *"Alex Gibney… is doing an AMA/Q&A in /r/movies today"*: "I organized an AMA/Q&A with Oscar-winning documentarian Alex Gibney… The AMA is live here now in r/movies for anyone interested in asking a question… He will be back after 2 PM ET today to answer questions."

## Hardest boundary: `question` vs. `complaint`

**Borderline post:** *"Musk - More Showtimes"*: "NYC based and spoiled with theater options, but somehow cannot find anymore Musk showings after work or on the weekend. Is it being phased out already? The Social Reckoning wasn't depressing enough for me that I'd like to sit through the 4 hours of this."

**Decision rule:** Apply these checks in order and stop at the first one that fits.

1. **`question`:** The post asks something another member could answer with a fact: a date, a policy, a yes/no, or "it's happening to me too." This includes "anyone else?" checks about a concrete problem (an app error, missing reservations), even when the tone is angry or the rest of the post is a review or news. Rhetorical questions don't count, and neither do requests to agree with an opinion ("Is it just me or are the recliners getting worse?", "Why do studios release so much at once?").
2. **`review`:** The post gives a verdict on a movie the poster saw (a rating, a recommendation, or a clear "good/bad"). Problems with the screening don't change this. If there's no verdict on the film, go to step 4.
3. **`psa`:** The post shares news or a fact meant for other members to use (a release date, a policy change, an event), even if the poster sounds annoyed about it.
4. **`complaint`:** Everything else that criticizes AMC, a studio, or the theater experience.

**Applied to the borderline post:** "Is it being phased out already?" can be answered with a fact, so *Musk - More Showtimes* is a `question`.

## Second boundary to watch: `review` vs. `complaint`

*"The first five minutes of FJORD"* is about a movie the poster saw, but the whole post criticizes the studio logos before the film. Step 2 of the decision rule covers it: there's no verdict on the film, so it's a `complaint`.

## Boundaries `psa` adds

- **`psa` vs. `question`:** *"Has AMC discontinued those cardboard popcorn boxes?"* reports news (a worker said the change "came from the top") but ends with "Has anyone else heard about this?"
- **`psa` vs. `complaint`:** stress-test #8 ("the 4-reservation limit now counts tickets you already checked into… Found out the hard way") shares a fact, but in an annoyed tone.

Both are covered by the decision rule above: the popcorn-box post is a `question` (step 1), and stress-test #8 is a `psa` (step 3).

## Hard cases from the stress test

- **"Has anyone else noticed the A-List price going up every year? Feels like they're squeezing loyal members."** It could be `question` or `complaint`. I chose `question` because the price increase can be checked (step 1), even though the post is mostly venting. Risk: "anyone else noticed…" vents could thin out `complaint`. I'll watch the counts in Milestone 4.
- **"Wildwood is a 9/10 for me… the sound was so loud it actually hurt, which knocked it down a point."** It could be `review` or `complaint`. I chose `review` because it gives a verdict on the film (9/10), and the screening problem doesn't change that. This case is why I reworded step 2 to look for a verdict instead of "the main point."

## Posts left out of the dataset

Mod and megathread posts, link or image-only posts, and posts that fit none of the three labels (for example the *"I think I have a problem"* concessions joke). _(Record roughly how many of these you skip; it's a finding about the community.)_
