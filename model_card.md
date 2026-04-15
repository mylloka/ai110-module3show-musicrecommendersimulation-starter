# Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder looks at a user's music preferences and picks the top 5 songs from a catalog that best match them.

The user tells the system what genre they like, what mood they want, and how energetic the music should feel. The system scores every song and returns the best matches with a short explanation.

It does not predict anything — it just ranks songs based on how well they fit the user's stated preferences.

---

## 3. Data Used

The catalog has **18 songs**. Each song has these features:

- **Genre** (like pop, lofi, rock, hip-hop, jazz)
- **Mood** (like happy, chill, intense, sad, peaceful)
- **Energy** — a number from 0.0 (very calm) to 1.0 (very loud and intense)
- **Valence** — a number from 0.0 (sad-sounding) to 1.0 (happy-sounding)
- **Acousticness** — a number from 0.0 (electronic/electric) to 1.0 (acoustic/unplugged)
- **Tempo**, **danceability** (collected but not used in scoring)

**Limits of the data:**
- 13 out of 15 genres have only one song each. That means users who ask for reggae, metal, or folk will always get the same song — there's nothing else to compare it to.
- All songs are Western and English-language. No K-pop, Afrobeats, Latin, or other global styles are included.
- Mood labels and feature values were assigned by hand. A real audio analysis tool might label them differently.

---

## 4. Algorithm Summary

The system gives each song a score out of 7.0 points. Higher score = better match.

Here's how the points are awarded:

| What it checks | Points if it matches |
|---|---|
| Genre matches the user's preference | +2.0 |
| Mood matches the user's preference | +1.0 |
| Energy is close to the user's target | up to +2.0 |
| Valence is close to the user's target | up to +1.0 |
| Acousticness is close to the user's target | up to +0.5 |

**Important:** For energy, valence, and acousticness, the system rewards *closeness*, not high or low values. A user who wants energy 0.4 will score a calm song (0.42) higher than a loud song (0.9), even though 0.9 is technically "more energy." The closer the song is to what the user asked for, the more points it gets.

After every song is scored, the system sorts them from highest to lowest and returns the top 5.

---

## 5. Observed Behavior / Biases

**The single-song genre trap.** 13 genres have only one song. Any user who asks for that genre will always get the same song at #1, every single time. It doesn't matter if the song's energy or mood is totally wrong — the genre bonus (+2.0) is so large that it usually wins anyway. A reggae listener always sees *Island Frequency*. A metal listener always sees *Iron Meridian*. There's no variety and no chance of discovering something new.

**Mood can get overruled by energy.** When a user asks for a sad song but also wants high energy, the system can't find one — because no song in the catalog is both high-energy and sad. So the high-energy songs win on points, and the sad song never shows up at #1. The algorithm is working correctly, but the catalog doesn't have what the user needs.

**Gym Hero keeps showing up for happy pop listeners.** A user asking for pop/happy gets *Sunrise City* at #1, which is correct. But *Gym Hero* (tagged pop/intense) keeps appearing in the top 5. Why? Because its energy (0.93) is very close to a high-energy target, and it gets the same genre bonus. The mood mismatch only costs it 1.0 point, which isn't enough to push it out of the top results.

---

## 6. Evaluation Process

Six user profiles were tested. Three were normal cases and three were designed to break or stress-test the system.

**Normal profiles:**
- **High-Energy Pop** (pop, happy, energy=0.88): *Sunrise City* hit #1. Correct.
- **Chill Lofi** (lofi, chill, energy=0.38): Three lofi songs competed. *Library Rain* won by a tiny margin on acousticness. The proximity formula worked exactly as intended.
- **Deep Intense Rock** (rock, intense, energy=0.92): *Storm Runner* hit #1 easily. Only one rock song exists, so no surprise.

**Edge case profiles:**
- **Genre Trap** (lofi genre + intense energy=0.93): The system was pulled in two directions. Lofi songs got the genre bonus but lost energy points. High-energy songs scored on energy but got no genre bonus. Neither group was a good match. The top result felt musically wrong.
- **Emotional Conflict** (rock, sad, energy=0.90): The only sad song in the catalog has low energy (0.44). It earned the mood bonus but lost on energy. *Storm Runner* won because energy + genre outweighed the mood match. Raising the mood weight to 2.0 still didn't fix it — the energy gap was too large.
- **Dead Center** (no genre/mood, everything at 0.50): No categorical bonuses fired. The "most average" song in the catalog won. This confirmed the numeric scoring works on its own.

A weight sensitivity test was also run: doubling the energy weight and halving the genre weight did not change the top 3 results for any of the normal profiles. Songs that scored well matched on multiple features at once, so single weight changes couldn't reorder them.

---

## 7. Intended Use and Non-Intended Use

**What this system is for:**
- A classroom exercise to explore how content-based filtering works
- Learning how scoring and ranking algorithms are built
- Testing what happens when user preferences conflict or edge cases appear

**What this system is NOT for:**
- Real music recommendations for real users
- Replacing Spotify, Apple Music, or any actual app
- Making decisions about what music people should or shouldn't hear
- Any use with more than a small educational dataset

This system has no collaborative filtering, no listening history, no user feedback loop, and only 18 songs. It should not be used as if it were a real product.

---

## 8. Ideas for Improvement

1. **Add more songs per genre.** Right now 13 of 15 genres have one song each. Adding 5–10 songs per genre would make the recommendations actually varied and interesting. A reggae user could get different recommendations depending on their energy target instead of always the same song.

2. **Add an `instrumentalness` feature.** Some people listen to music while studying or working and need no vocals. Right now the system can't tell the difference between a lofi track with distracting lyrics and a pure instrumental one. Adding this feature would make recommendations much better for focus and study use cases.

3. **Add a diversity penalty.** For the lofi/chill profile, the top 5 results are often nearly identical — three very similar calm songs. A penalty that lowers a song's score if something very similar is already in the top results would force more variety into the recommendations.

---

## 9. Personal Reflection

**Biggest learning moment**

I expected the formula to be the hard part. It wasn't. The hardest part was the catalog. When I ran the edge case profiles, I kept thinking "the algorithm must be wrong" — but every time I checked the math, the algorithm was doing exactly what I told it to. The problem was that the catalog didn't have a song that matched what the user wanted. A sad high-energy rock song doesn't exist in 18 songs. No formula fix can recommend something that isn't there. That was the moment I understood why Spotify has 100 million tracks. The algorithm is almost secondary.

**How AI tools helped — and when I had to double-check**

AI helped me move fast. When I needed the proximity formula, the scoring weights, or the CSV expansion, I got working code quickly instead of spending an hour on syntax. But I had to check the output every time. At one point the tool generated songs with feature values that looked plausible but weren't consistent with the mood labels — a "peaceful" song with energy 0.85 doesn't make sense. I had to read the data manually and fix those. AI is good at writing code that runs. It's not automatically good at writing data that makes sense.

**What surprised me about simple algorithms feeling like recommendations**

I thought a real recommendation would need machine learning, user history, and something complex under the hood. But when I ran the High-Energy Pop profile and *Sunrise City* came out #1, it genuinely felt correct. It matched what I would have chosen by hand. A few `if` statements and some subtraction produced something that felt intelligent. That was surprising. It made me realize that "feeling like a recommendation" mostly means "matching what the user asked for" — and even a simple formula can do that when the preferences are clear and the catalog has the right song.

**What I'd try next**

I'd add collaborative filtering on top of this. Right now the system only knows what the user *says* they like. A real next step would be tracking which recommendations the user actually plays, skips, or replays — and using that to update the weights automatically. If a user always skips high-energy songs even when they asked for them, the system should learn that. That's the gap between this simulation and how Spotify actually works.
