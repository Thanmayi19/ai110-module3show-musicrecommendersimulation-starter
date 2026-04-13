import csv
import math
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

def load_songs(csv_path: str) -> List[Song]:
    """Read a CSV at csv_path and return a list of Song dataclass instances with all fields type-cast."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(Song(
                id=int(row["id"]),
                title=row["title"],
                artist=row["artist"],
                genre=row["genre"],
                mood=row["mood"],
                energy=float(row["energy"]),
                tempo_bpm=float(row["tempo_bpm"]),
                valence=float(row["valence"]),
                danceability=float(row["danceability"]),
                acousticness=float(row["acousticness"]),
            ))
    return songs

def score_song(user_prefs: Dict, song: Song) -> Tuple[float, List[str]]:
    """Score song against user_prefs using categorical and Gaussian signals; return (total_score, reasons)."""
    total = 0.0
    reasons = []

    # Genre match — categorical, case-insensitive (+1.0)  # EXPERIMENT: was +2.0
    if song.genre.lower() == user_prefs["favorite_genre"].lower():
        total += 1.0  # EXPERIMENT: was 2.0
        reasons.append("Genre match (+1.0)")

    # Mood match — categorical, case-insensitive (+1.0)
    if song.mood.lower() == user_prefs["favorite_mood"].lower():
        total += 1.0
        reasons.append("Mood match (+1.0)")

    # Energy proximity — Gaussian with σ = 0.2, max +2.0  # EXPERIMENT: multiplier was 1.0 (no multiply), now 2.0
    energy_score = 2.0 * math.exp(  # EXPERIMENT: was math.exp(...) with no multiplier
        -((song.energy - user_prefs["target_energy"]) ** 2) / (2 * 0.2 ** 2)
    )
    total += energy_score
    reasons.append(f"Energy match (+{energy_score:.2f})")

    # Tempo proximity — Gaussian with σ = 20 BPM, both values normalized to 0–1 by /200
    song_tempo_norm = song.tempo_bpm / 200
    user_tempo_norm = user_prefs["target_tempo_bpm"] / 200
    tempo_score = math.exp(
        -((song_tempo_norm - user_tempo_norm) ** 2) / (2 * (20 / 200) ** 2)
    )
    total += tempo_score
    reasons.append(f"Tempo match (+{tempo_score:.2f})")

    # Danceability proximity — Gaussian with σ = 0.2, scaled to max +0.5
    danceability_score = 0.5 * math.exp(
        -((song.danceability - user_prefs["target_danceability"]) ** 2) / (2 * 0.2 ** 2)
    )
    total += danceability_score
    reasons.append(f"Danceability match (+{danceability_score:.2f})")

    return total, reasons


def recommend_songs(user_prefs: Dict, songs: List[Song], k: int = 5) -> List[Tuple[float, List[str], Song]]:
    """Score all songs against user_prefs and return the top k as (score, reasons, song) tuples, highest first."""
    scored = [
        (score, reasons, song)
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[0], reverse=True)[:k]
