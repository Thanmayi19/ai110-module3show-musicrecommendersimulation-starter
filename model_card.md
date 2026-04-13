# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
**TuneMatch 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

## This model suggests up to 5 songs from an 18-song catalog based on a user's preferred genre, mood, energy level, tempo, and danceability. It is built for classroom exploration of how recommender systems work not for real users or production use. It assumes the user can describe their preferences numerically and that a single "favorite genre" accurately captures their taste.

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song in the catalog gets a score based on how closely it matches what the user said they like. Genre and mood are checked as exact matches if your favorite genre is pop and a song is pop, it gets bonus points. If not, it gets nothing for that category.

The remaining points come from how close each song's energy, tempo, and danceability are to your targets. Instead of a hard cutoff, the system uses a bell curve songs right at your preferred energy score highest, and songs further away score progressively less. All songs are ranked by their total score, and the top 5 are returned.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

## The catalog contains 18 songs across 12 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, metal, r&b, electronic, and country. Moods represented include happy, chill, intense, relaxed, moody, focused, melancholic, romantic, aggressive, euphoric, and sad. No songs were removed from the starter dataset. The data skews toward Western popular music styles and does not represent non-Western genres, non-English language music, or niche subgenres. Lofi is the most represented genre with 3 songs; most genres have only 1 representative.

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

## The system works well for users whose preferences sit in the middle of the catalog's range moderate energy, common genres like pop or jazz. The scoring is fully transparent: every recommendation comes with a reasons list explaining exactly which signals contributed and how much. The genre and mood gates act as strong, intuitive anchors if a user asks for jazz, jazz songs reliably appear at the top as long as their continuous preferences don't conflict heavily.

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

Genre filter bubble. Genre matching is binary, a pop fan will never see an indie pop or synthwave song even when it would be a closer stylistic match than a same-genre song with mismatched energy. There is no partial credit for related genres.

Edge-preference penalty. The bell-curve scoring assumes the catalog has songs on both sides of the user's target. Users who prefer very low or very high energy (0.0 or 1.0) are silently penalized because the catalog's range doesn't extend that far, so their best available match still loses points.

Genre frequency imbalance. Lofi has 3 songs while most genres have only 1. A lofi user's top 5 results can be filled mostly with lofi songs, crowding out variety. An electronic or metal user only ever gets one genre-match bonus, making their results structurally weaker.

Single-mood and single-genre inputs. The system assumes every user has exactly one favorite genre and one favorite mood. Users who enjoy variety, whose taste crosses genres, or who don't care about mood at all are not well served. There is no way to say "mood doesn't matter" or "I like both jazz and r&b."

## No diversity enforcement. The top-k selection is purely greedy, the highest-scoring songs win, even if they are all by the same artist or in the same genre.

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

I tested five adversarial user profiles designed to stress-test the scoring logic:

Ghost genre (k-pop): confirmed the genre bonus is silently unreachable, capping max score at 3.5 instead of 5.5 with no warning.
Energy floor (target_energy=0.01): the closest song (Autumn Sonata, energy 0.25) still lost nearly half its energy points despite being the best available match.
Conflicting signals (metal genre + chill/low-energy preferences): the genre bonus for Blood and Thunder was nearly wiped out by its Gaussian penalty, and calmer songs outranked it.
Hypersonic tempo (300 BPM): normalizing to > 1.0 caused every song's tempo score to collapse to near zero, the signal vanished silently.
All-zeros input: no crash, but scores were uniformly depressed and indistinguishable from a user who genuinely preferred energy 0.25.
None of these crashed the system, but all produced misleading-looking results with no feedback to the caller.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

Partial genre credit using a genre affinity map so stylistically related genres receive a fractional bonus rather than zero.
Catalog-aware clamping for Gaussian inputs, so a user who prefers extreme energy is compared against the closest available song rather than penalized for the catalog's boundaries.
Genre cap in top-k (e.g., at most 2 songs per genre) to enforce diversity without changing the scoring logic.
Optional mood field so users who don't have a mood preference aren't forced to pick one.
Larger and more balanced catalog at least 4–5 songs per genre to let the continuous signals meaningfully differentiate within a genre.
Multi-genre preferences so a user can express "I like both jazz and ambient" and receive partial credit for each.

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

Building this recommender made me realize how much a simple number like a genre weight quietly shapes what a user gets to discover. I expected the system to feel "fair" once the math was working, but testing adversarial profiles showed how a 36% weight on genre alone can turn a recommendation engine into an echo chamber, a metal fan asking for something chill still gets metal, even when calmer songs would have been a better fit. The most surprising moment was the hypersonic tempo test: setting tempo to 300 BPM didn't crash anything, it just silently erased the tempo signal from every result, which made me think about how real systems can fail invisibly without any error to catch. Working through the bias analysis changed how I think about apps like Spotify what looks like a personalized recommendation is really just a weighted scoring function, and whoever chose those weights decided what kinds of listeners the system serves well and which ones it quietly underserves.
