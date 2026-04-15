from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV catalog and return each row as a typed dict with numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Apply the Algorithm Recipe to one song and return (total_score, reasons) where max score is 7.0."""
    score = 0.0
    reasons = []

    # --- Categorical matches ---
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre '{song['genre']}' matches (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood '{song['mood']}' matches (+1.0)")

    # --- Numeric proximity scores (reward closeness, not magnitude) ---
    if "energy" in user_prefs:
        proximity = 1 - abs(song["energy"] - user_prefs["energy"])
        pts = round(2.0 * proximity, 2)
        score += pts
        if proximity >= 0.85:
            reasons.append(f"energy {song['energy']} is close to your target {user_prefs['energy']} (+{pts})")

    if "valence" in user_prefs:
        proximity = 1 - abs(song["valence"] - user_prefs["valence"])
        pts = round(1.0 * proximity, 2)
        score += pts

    if "acousticness" in user_prefs:
        proximity = 1 - abs(song["acousticness"] - user_prefs["acousticness"])
        pts = round(0.5 * proximity, 2)
        score += pts

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog, sort by score descending, and return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "general audio similarity"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
