"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from recommender import load_songs, recommend_songs


def print_results(label: str, user_prefs: dict, recommendations: list) -> None:
    """Print a formatted results block for one user profile."""
    print("\n" + "=" * 60)
    print(f"  {label}")
    print("=" * 60)
    prefs_line = " | ".join(f"{k}={v}" for k, v in user_prefs.items())
    print(f"  Profile : {prefs_line}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  (Score: {score:.2f} / 7.0)")
        print(f"       Artist : {song['artist']}")
        print(f"       Genre  : {song['genre']}  |  Mood : {song['mood']}")
        print(f"       Why    : {explanation}")
        print("  " + "-" * 58)
    print()


def main() -> None:
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(data_path)
    print(f"Loaded songs: {len(songs)}")

    # ── Standard Profiles ───────────────────────────────────────────────

    profiles = [
        (
            "Profile 1 — High-Energy Pop",
            {"genre": "pop", "mood": "happy",   "energy": 0.88, "valence": 0.85, "acousticness": 0.10},
        ),
        (
            "Profile 2 — Chill Lofi",
            {"genre": "lofi", "mood": "chill",  "energy": 0.38, "valence": 0.58, "acousticness": 0.82},
        ),
        (
            "Profile 3 — Deep Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.92, "valence": 0.42, "acousticness": 0.08},
        ),

        # ── Adversarial / Edge-Case Profiles ────────────────────────────

        # Conflict: genre=lofi implies calm; energy=0.93 implies intense.
        # Does the +2.0 genre bonus keep surfacing low-energy lofi tracks
        # even though the energy is completely wrong?
        (
            "EDGE 1 — Genre Trap  (lofi label + intense energy)",
            {"genre": "lofi", "mood": "intense", "energy": 0.93, "valence": 0.75, "acousticness": 0.12},
        ),

        # Conflict: energy=0.90 suggests an aggressive track; mood=sad
        # suggests a slow, mournful one. Only one song in the catalog
        # (Last Highway Home) is tagged sad — does it rank despite having
        # energy=0.44, far from the target?
        (
            "EDGE 2 — Emotional Conflict  (high energy + sad mood)",
            {"genre": "rock", "mood": "sad",     "energy": 0.90, "valence": 0.28, "acousticness": 0.08},
        ),

        # Dead center: no genre, no mood — pure numeric averaging at 0.50.
        # No categorical bonus will ever fire. Exposes which song is most
        # "average" across the catalog.
        (
            "EDGE 3 — Dead Center  (no genre/mood, all features at 0.50)",
            {"energy": 0.50, "valence": 0.50, "acousticness": 0.50},
        ),
    ]

    for label, user_prefs in profiles:
        recs = recommend_songs(user_prefs, songs, k=5)
        print_results(label, user_prefs, recs)


if __name__ == "__main__":
    main()
