"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys
from src.recommender import load_songs, recommend_songs

# Force UTF-8 output so unicode block characters render on all platforms
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

WIDTH = 52
MAX_SCORE = 5.5   # EXPERIMENT: 1.0 genre + 1.0 mood + 2.0 energy + 1.0 tempo + 0.5 danceability
BAR_WIDTH = 20    # number of block characters at full score


def score_bar(score: float, max_score: float = MAX_SCORE, width: int = BAR_WIDTH) -> str:
    filled = round((score / max_score) * width)
    return "█" * filled + "░" * (width - filled)


def print_banner(user_prefs: dict, catalog_size: int) -> None:
    print("=" * WIDTH)
    print("MUSIC RECOMMENDER".center(WIDTH))
    print("=" * WIDTH)
    print(f"  Genre   : {user_prefs['favorite_genre'].title()}")
    print(f"  Mood    : {user_prefs['favorite_mood'].title()}")
    print(f"  Energy  : {user_prefs['target_energy']:.2f}")
    print(f"  Tempo   : {user_prefs['target_tempo_bpm']} BPM")
    print(f"  Dance   : {user_prefs['target_danceability']:.2f}")
    print(f"  Catalog : {catalog_size} songs")
    print("=" * WIDTH)


def print_result(rank: int, score: float, reasons: list, song) -> None:
    print(f"\n  #{rank}  {song.title} — {song.artist}")
    print(f"       {score:.2f} / {MAX_SCORE:.2f}  [{score_bar(score)}]")
    for reason in reasons:
        print(f"       • {reason}")


def print_footer(recommendations: list) -> None:
    print("\n" + "─" * WIDTH)
    top_score, _, top_song = recommendations[0]
    print(f"  Top pick  : {top_song.title} ({top_score:.2f} pts)")
    avg = sum(s for s, _, _ in recommendations) / len(recommendations)
    print(f"  Avg score : {avg:.2f} / {MAX_SCORE:.2f}")
    print(f"  Showing   : {len(recommendations)} of top results")
    print("─" * WIDTH + "\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
    "favorite_genre": "ambient",
    "favorite_mood": "chill",
    "target_energy": 0.0,
    "target_tempo_bpm": 0,
    "target_danceability": 0.0,
    }


    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_banner(user_prefs, len(songs))

    for rank, (score, reasons, song) in enumerate(recommendations, start=1):
        print_result(rank, score, reasons, song)
        if rank < len(recommendations):
            print("\n" + "─" * WIDTH)

    print_footer(recommendations)


if __name__ == "__main__":
    main()
