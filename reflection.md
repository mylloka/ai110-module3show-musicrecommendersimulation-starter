# Reflection: Profile Comparisons

This file compares pairs of user profiles from the recommender experiments and explains what changed between them and why it makes sense.

---

## Profile 1 vs Profile 2 — High-Energy Pop vs Chill Lofi

**Pop profile** (energy=0.88, valence=0.85, acousticness=0.10): The top results were loud, fast, electric songs. *Sunrise City* scored #1 because it is pop, it is happy, and its energy (0.82) is close to 0.88. The system avoided quiet or acoustic songs because their energy was far from the target — they lost almost 2 full points just for being calm.

**Lofi profile** (energy=0.38, valence=0.58, acousticness=0.82): The top results were quiet, mellow, acoustic songs. *Library Rain* scored #1 because it is lofi, it is chill, and its acousticness (0.86) is very close to 0.82. The system pushed away anything with high energy.

**Why it makes sense:** Energy is the heaviest numeric feature (worth up to 2.0 points). When the target energy flips from 0.88 down to 0.38, the entire ranking flips with it. Songs that were near-perfect for the pop listener are near-worthless for the lofi listener. This is the proximity formula working correctly — it does not reward high energy, it rewards closeness to whatever the user asked for.

---

## Profile 1 vs Profile 3 — High-Energy Pop vs Deep Intense Rock

**Pop profile** (genre=pop, mood=happy): *Sunrise City* is #1, *Gym Hero* is nearby. Both are high-energy, but *Sunrise City* has mood=happy which matches the profile — *Gym Hero* is tagged "intense" and gets no mood bonus.

**Rock profile** (genre=rock, mood=intense, energy=0.92): *Storm Runner* is #1. It has the rock genre match (+2.0), the intense mood match (+1.0), and energy=0.91 which is nearly identical to 0.92. *Gym Hero* also appears in the top 5 because its energy (0.93) is close to 0.92 and it is intense — but it is pop not rock, so it loses the genre bonus.

**Why it makes sense:** Both profiles want high-energy music, so many of the same songs appear in both top 5 lists. The difference is the genre and mood tags pushing different songs to #1. This shows that the categorical bonuses (genre and mood) act as tiebreakers between songs with similar numeric features. If two songs have nearly the same energy, the one that matches the user's genre wins.

---

## Profile 2 vs EDGE 1 — Chill Lofi vs Genre Trap

**Chill Lofi** (genre=lofi, mood=chill, energy=0.38): A consistent, sensible result. All three lofi songs cluster at the top because they share the genre bonus, the mood bonus, and naturally low energy.

**Genre Trap** (genre=lofi, mood=intense, energy=0.93): The result is confusing and unsatisfying. Lofi songs get the +2.0 genre bonus but their energy is 0.35–0.42, so they lose almost the entire 2.0 energy points. Non-lofi songs like *Gym Hero* or *Storm Runner* score well on energy but receive no genre bonus. The system cannot find a lofi+intense song because one does not exist in the catalog.

**Why it makes sense:** This is a catalog gap, not a formula bug. The formula is doing exactly what it is supposed to — adding up how well each feature matches. The problem is that no song in the catalog is both lofi and intense. Real Spotify does not have this problem because it has millions of songs. A small 18-song catalog cannot cover every combination, and when a user asks for a rare combination, the system has nothing to give them.

---

## Profile 3 vs EDGE 2 — Deep Intense Rock vs Emotional Conflict

**Deep Intense Rock** (genre=rock, mood=intense, energy=0.92): Clean result. *Storm Runner* is #1 because rock+intense+high energy all point to the same song.

**Emotional Conflict** (genre=rock, mood=sad, energy=0.90): *Storm Runner* is still #1, even though the user wanted a sad song. *Last Highway Home* is the only sad-tagged song, but it has energy=0.44 — almost half a point away from the 0.90 target. That gap costs it nearly 1.0 point in the energy score. *Storm Runner* wins because genre and energy combined are worth more than one mood match.

**Why it makes sense:** Think of it like a points game. The sad song gets +1.0 for mood. But the rock song gets +2.0 for genre plus nearly +2.0 for energy — that is almost 4 points before valence or acousticness are even counted. The sad song cannot catch up unless there is a song in the catalog that is both sad and high-energy. There is not. This is the same reason why real apps sometimes recommend a song that does not "feel right" — the algorithm found the best match it could, but the best match in that catalog is still not a good match.

---

## EDGE 1 vs EDGE 3 — Genre Trap vs Dead Center

**Genre Trap** (genre=lofi, mood=intense): Has strong categorical preferences that conflict with each other. The results feel messy because the system is being pulled in two directions at once.

**Dead Center** (no genre/mood, energy=0.50, valence=0.50, acousticness=0.50): No genre, no mood, everything at 0.50. No categorical bonus ever fires. The winner is simply the song with audio features closest to the mathematical center of the 0–1 scale. The result is stable and predictable — but it also reveals that without any personal taste signal, the system defaults to "average," which is not the same as "good."

**Why it makes sense:** The Genre Trap shows what happens when a user's preferences exist but conflict. The Dead Center shows what happens when a user has no preferences at all. In both cases the recommender struggles — but for opposite reasons. Genre Trap has too much conflicting signal; Dead Center has no signal. A good recommender needs clear, consistent preferences to produce good results, just like a music streaming app needs listening history before its recommendations start making sense.

---

## Why "Gym Hero" Keeps Showing Up for Happy Pop Listeners

Imagine you tell a music recommender: "I like pop music that makes me feel happy." The recommender looks at every song and adds up points.

*Sunrise City* is tagged pop and happy — it gets 2 points for genre and 1 point for mood right away. That is a 3-point head start before energy or tempo are even considered.

*Gym Hero* is also tagged pop, so it gets the same 2-point genre bonus. Its mood is "intense" not "happy," so it misses the 1-point mood bonus. But *Gym Hero* has energy=0.93, which is very close to what a high-energy pop listener wants (0.88). That closeness earns it nearly 2 more points.

So *Gym Hero* ends up with about 4 points (genre + high energy) while *Sunrise City* ends up with about 5 points (genre + mood + decent energy). *Sunrise City* wins — but *Gym Hero* is close enough to appear in the top 5 every time.

This happens because energy is the largest numeric weight in the formula. A song that is close on energy will always be competitive, even if its mood is wrong. For a user who cares deeply about the "happy" feeling, this is a bad result — the system served them an intense gym track. For a user who just wants upbeat music and doesn't care about the mood label, it might be fine. The formula cannot tell the difference because it treats all profiles the same way.
