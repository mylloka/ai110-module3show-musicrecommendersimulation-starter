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


def main() -> None:
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(data_path)
    print(f"Loaded songs: {len(songs)}")

    # Default profile: upbeat pop listener
    user_prefs = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.80,
        "valence":      0.80,
        "acousticness": 0.20,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # ── Header ──────────────────────────────────────────────────────────
    print("\n" + "=" * 56)
    print("   Music Recommender — Top 5 Results")
    print("=" * 56)
    print(f"  Profile : genre={user_prefs['genre']} | mood={user_prefs['mood']}")
    print(f"            energy={user_prefs['energy']} | valence={user_prefs['valence']} | acousticness={user_prefs['acousticness']}")
    print("=" * 56)

    # ── Results ─────────────────────────────────────────────────────────
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  (Score: {score:.2f} / 7.0)")
        print(f"       Artist : {song['artist']}")
        print(f"       Genre  : {song['genre']}  |  Mood : {song['mood']}")
        print(f"       Why    : {explanation}")
        print("  " + "-" * 54)

    print()


if __name__ == "__main__":
    main()
