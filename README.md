# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This simulation builds a content-based music recommender that scores every song in a small catalog against a user's taste profile and returns the top matches. It prioritizes three numeric audio features — energy, valence, and acousticness — combined with categorical bonuses for matching mood and genre. The system is transparent by design: every recommendation includes a plain-language explanation of exactly why each song was selected.

---

## How The System Works

Explain your design in plain language.

Real-world recommenders like Spotify combine collaborative filtering (learning from what similar users liked) and content-based filtering (matching song attributes to a user's taste). This simulation focuses on content-based filtering — it compares measurable song properties directly against a user's stated preferences, so it works immediately without any listening history. This version prioritizes energy and emotional tone above genre, because those two features most directly capture how a song feels in the moment.

**Song features used:** `genre`, `mood`, `energy`, `valence`, `acousticness`, `tempo_bpm`, `danceability`

**UserProfile fields used:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

```mermaid
flowchart TD
    A([INPUT\nUser Preferences\ngenre · mood · energy · valence · acousticness])
    A --> B[load_songs\nReads data/songs.csv]
    B --> C[18 song dicts\nloaded into memory]
    C --> D

    subgraph LOOP [PROCESS — score_song called for every song]
        direction TB
        D[Pick next song from catalog]
        D --> E[Genre match? +2.0 pts]
        E --> F[Mood match? +1.0 pts]
        F --> G[Energy proximity\n2.0 × 1 − difference]
        G --> H[Valence proximity\n1.0 × 1 − difference]
        H --> I[Acousticness proximity\n0.5 × 1 − difference]
        I --> J[Sum all points\nmax score = 7.0]
        J --> K[Append song · score · reason\nto scored list]
    end

    K --> L{All 18 songs\nscored?}
    L -- No --> D
    L -- Yes --> M[Sort scored list\nby score descending]
    M --> N[Slice top-k results]
    N --> O([OUTPUT\nPrint title · score · explanation])
```

---

### Finalized Algorithm Recipe

Every song in the catalog is scored using this formula. Points are added up and the highest-scoring songs are returned first.

| Rule | Points | Condition |
|---|---|---|
| Genre match | **+2.0** | `song.genre == user.genre` (exact string match) |
| Mood match | **+1.0** | `song.mood == user.mood` (exact string match) |
| Energy proximity | **up to +2.0** | `2.0 × (1 − \|song.energy − user.energy\|)` |
| Valence proximity | **up to +1.0** | `1.0 × (1 − \|song.valence − user.valence\|)` |
| Acousticness proximity | **up to +0.5** | `0.5 × (1 − \|song.acousticness − user.acousticness\|)` |
| **Max possible score** | **7.0** | All five rules fire at full value |

The proximity formula rewards closeness, not magnitude — a song with energy 0.44 scores higher than one with energy 0.93 for a user whose target energy is 0.42, because 0.44 is *closer*.

**User profile used in this simulation:**

```python
user_prefs = {
    "genre":        "lofi",
    "mood":         "focused",
    "energy":       0.42,
    "valence":      0.60,
    "acousticness": 0.75,
}
```

---

### Potential Biases

- **Genre dominance.** A genre match alone adds +2.0 points — the single largest bonus available. A lofi song with a poor energy match can still outscore a perfect-energy jazz track simply because of its label. This means the system may surface mediocre matches within the preferred genre before excellent matches outside it.

- **Mood sparsity.** With `mood = "focused"`, the +1.0 bonus fires for only one song in the original catalog (Focus Flow). Most songs never earn a mood bonus, so mood ends up having less influence than its weight suggests. A user whose mood is rare in the catalog is effectively scored on four features, not five.

- **Double-penalizing high-energy songs.** Energy and acousticness are strongly inversely correlated in this dataset — high-energy songs are almost always low-acoustic. For a chill user (low energy, high acousticness), both features penalize the same tracks simultaneously, making the system harsher toward energetic songs than either weight alone implies.

- **Thin genre coverage.** After expansion, genres like metal, classical, folk, and reggae each have only one representative song. Even if those genres are a reasonable fit, the system has no room to find a *good* representative — it either returns that one song or nothing from that genre.

- **No vocal awareness.** The system cannot distinguish between vocal and instrumental tracks. For a `focused` study user, instrumental lofi is meaningfully different from vocal lofi, but both score identically on every numeric feature.

---

## Sample Output

Terminal output when running `python src/main.py` with the default `pop / happy` profile:

```
Loaded songs: 18

========================================================
   Music Recommender — Top 5 Results
========================================================
  Profile : genre=pop | mood=happy
            energy=0.8 | valence=0.8 | acousticness=0.2
========================================================

  #1  Sunrise City  (Score: 6.41 / 7.0)
       Artist : Neon Echo
       Genre  : pop  |  Mood : happy
       Why    : genre 'pop' matches (+2.0); mood 'happy' matches (+1.0); energy 0.82 is close to your target 0.8 (+1.96)
  ------------------------------------------------------

  #2  Gym Hero  (Score: 5.13 / 7.0)
       Artist : Max Pulse
       Genre  : pop  |  Mood : intense
       Why    : genre 'pop' matches (+2.0); energy 0.93 is close to your target 0.8 (+1.74)
  ------------------------------------------------------

  #3  Rooftop Lights  (Score: 4.34 / 7.0)
       Artist : Indigo Parade
       Genre  : indie pop  |  Mood : happy
       Why    : mood 'happy' matches (+1.0); energy 0.76 is close to your target 0.8 (+1.92)
  ------------------------------------------------------

  #4  Crown Protocol  (Score: 3.16 / 7.0)
       Artist : Verse Division
       Genre  : hip-hop  |  Mood : confident
       Why    : energy 0.72 is close to your target 0.8 (+1.84)
  ------------------------------------------------------

  #5  Night Drive Loop  (Score: 3.08 / 7.0)
       Artist : Neon Echo
       Genre  : synthwave  |  Mood : moody
       Why    : energy 0.75 is close to your target 0.8 (+1.9)
  ------------------------------------------------------
```

**Why these results make sense:** Sunrise City earns the maximum available bonus points — it matches genre, mood, and energy simultaneously. Gym Hero ranks second because the genre match (+2.0) outweighs its missing mood bonus. Rooftop Lights reaches #3 through the mood match alone, despite being labelled `indie pop` rather than `pop`. Songs #4 and #5 have no categorical matches at all — they rank purely on how close their energy is to the user's target of 0.80.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

