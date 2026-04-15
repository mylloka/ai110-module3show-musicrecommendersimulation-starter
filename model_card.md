# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 generates top-5 song recommendations from an 18-song catalog based on a user's stated taste profile. It is designed for classroom exploration of content-based filtering — not for real users or production deployment. The system assumes the user can describe their preferences in advance using genre, mood, and numeric audio targets. It does not learn from listening history or adapt over time.

---

## 3. How the Model Works

Every song in the catalog is compared to the user's taste profile and awarded points based on how well it matches. A song earns bonus points if its genre or mood label exactly matches what the user asked for. It also earns points based on how close its audio features — energy level, emotional tone (valence), and acoustic texture — are to the user's targets. Closeness is rewarded, not just high or low values: a calm user who wants energy 0.4 will score a song at 0.42 higher than one at 0.9, even though 0.9 is technically "more." After every song is scored, they are sorted from highest to lowest, and the top five are returned with a plain-language explanation of why each one ranked where it did.

---

## 4. Data

The catalog contains 18 songs across 15 genres and 14 mood labels. The original 10-song starter dataset was expanded by 8 songs to cover genres and moods not present in the default file, including hip-hop, classical, metal, r&b, folk, country, EDM, and reggae. Despite the expansion, 13 of 15 genres have exactly one representative song, and lofi is the only genre with three songs. The dataset reflects a Western, English-language view of music genres and does not represent K-pop, Afrobeats, Latin music, or non-Western traditions. Mood labels and audio feature values were assigned manually and may not match how a real music analysis tool would classify the same tracks.

---

## 5. Strengths

The system works best for users whose preferences align with well-represented catalog areas. A lofi/chill listener receives clearly differentiated top results because three lofi songs exist to compete for ranking. A pop/happy or rock/intense listener also gets a clean top result because those genre+mood combinations map to a unique song. The scoring produces transparent, human-readable explanations for every result, which makes it easy to understand why a recommendation was made. The proximity formula correctly handles the "closeness not magnitude" problem — a moderately energetic user is not always pushed toward the highest-energy songs.

---

## 6. Limitations and Bias

**Primary weakness — single-song genre filter bubble.** Thirteen of the fifteen genres in this catalog have exactly one representative song. This means any user whose preferred genre is not lofi, pop, or rock will always receive the same song as their genre-matched #1 recommendation, with no variety possible. A reggae listener will always see Island Frequency at the top; a metal listener will always see Iron Meridian. Because the genre bonus (+2.0 points) is the largest single weight in the scoring formula, that one song will dominate the results every time that genre is requested — regardless of whether the song's energy, mood, or valence actually matches the user's preferences. This is a structural filter bubble: the system does not expose users to anything new within their genre because there is nothing else to show them. A real recommender with this design would need at minimum five to ten songs per genre before genre-based ranking produces meaningful differentiation. Beyond genre coverage, the system also cannot distinguish vocal from instrumental tracks, which matters significantly for users who listen to music while studying or working — two lofi tracks with identical feature values will always score identically even if one has distracting vocals and the other does not.

---

## 7. Evaluation

Six user profiles were tested: three standard and three adversarial edge cases.

**Standard profiles (results matched musical intuition):**

- **High-Energy Pop** (genre=pop, mood=happy, energy=0.88, valence=0.85, acousticness=0.10): *Sunrise City* scored #1. It is the only pop song in the catalog, so the +2.0 genre bonus locked it in place. *Gym Hero* (pop/intense) appeared in the top 5 but ranked lower because its mood tag is "intense" rather than "happy." What was surprising: *Gym Hero* still crept into the top results despite being tagged intense, purely because its energy (0.93) is so close to the target. Genre and energy together overpower mood when a song matches both.
- **Chill Lofi** (genre=lofi, mood=chill, energy=0.38, valence=0.58, acousticness=0.82): Three lofi songs competed for the top spots — the only profile with real within-genre variety. *Library Rain* edged out *Midnight Coding* by a fraction because its acousticness (0.86) was slightly closer to the target (0.82). This showed the proximity formula doing exactly what it should.
- **Deep Intense Rock** (genre=rock, mood=intense, energy=0.92, valence=0.42, acousticness=0.08): *Storm Runner* reached #1 easily. It is the only rock song and its energy (0.91) nearly matches the target. No surprises here — single-song genres always produce a predictable #1.

**Adversarial profiles (revealed structural weaknesses):**

- **EDGE 1 — Genre Trap** (genre=lofi, mood=intense, energy=0.93): The system split: lofi songs received the genre bonus but their low energy (0.35–0.42) was far from the 0.93 target, costing them nearly the full 2.0 energy points. High-energy non-lofi songs scored on energy but received no genre bonus. Neither group fully satisfied the profile. The result was a muddled top 5 where #1 was a lofi song that felt musically wrong for an intense listener.
- **EDGE 2 — Emotional Conflict** (genre=rock, mood=sad, energy=0.90): *Last Highway Home* is the only sad-tagged song in the catalog (energy=0.44). It received +1.0 for mood but lost nearly 1.8 energy points because its energy was 0.46 away from the 0.90 target. *Storm Runner* scored higher despite having no sad mood tag, because its energy (0.91) was nearly perfect and it had the genre match. The sad song never reached #1. Raising the mood weight to 2.0 did not change the result — the energy gap was too large.
- **EDGE 3 — Dead Center** (no genre/mood, all features at 0.50): No categorical bonus ever fired. The winner was the song closest to average across all three numeric features. This exposed which song is most "middle of the road" in the catalog — a useful test for confirming the numeric scoring works independently of the genre/mood bonuses.

A weight sensitivity test on the standard profiles confirmed that doubling the energy weight and halving the genre weight did not change any top-3 ranking — songs that scored well already matched on multiple features, making them resilient to weight adjustments.

---

## 8. Future Work

The most impactful improvement would be adding five to ten songs per genre to eliminate the single-song filter bubble. Beyond data, the scoring logic could incorporate `instrumentalness` from the Spotify audio features API to serve focus and study listeners better. A diversity penalty — where the system downgrades a song if a very similar one is already in the top results — would prevent the top five from being dominated by nearly identical lofi tracks for chill profiles. Finally, a two-stage approach that first filters to candidate songs within a reasonable energy range, then ranks by all features, would prevent wildly mismatched songs from cluttering lower-ranked positions.

---

## 9. Personal Reflection

Building this simulation made it clear that the most important part of a recommender is not the scoring formula — it is the catalog. A perfect formula applied to a thin, uneven dataset produces thin, uneven recommendations. The experiment that surprised me most was the weight sensitivity test: doubling the energy weight changed nothing about the top-3 order. I expected bigger shifts, but the songs that scored well already matched on multiple features at once, making them resilient to weight changes. This changed how I think about the "algorithm" as the source of recommendation quality in real apps like Spotify. The algorithm matters, but the real work happens in the data — the millions of user-generated playlists and audio features that let collaborative and content-based signals reinforce each other in ways a 18-song toy system simply cannot replicate.
