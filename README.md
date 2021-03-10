# Spotify Song Genre Classification

***

Project Goal: "Maximize the micro-averaged ROC curve for the classification of song genres"

Data was obtained from the following sources:
- [Spotify Song Data](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks)
- [Genius Lyric Data (Requires an API key)](https://api.genius.com)

***

## Data Matching (Attempt 1)
See `info_rnd1_dataclean.ipynb`.

## Data Matching (Attempt 2)
Instead of incrementally decreasing the size of the dataset, I will leave null values for songs I could not find lyrics for instead of removing the record. I will use partial ratio similarity like the later rounds of my first attempt.
After fixing the matching algorithm, I had the following results:
- 85,515 songs matched (50.01%)

My similarity threshold of 80 was a good estimator, as the distribution of similarities drops off significantly after that point, and non-matches become more common. 

## Genre merging
Using the results from my first run at data cleaning, I found that ~410 genres represent around 90% of the genre sample space. (TODO: Check that these assumptions hold after the second data cleaning)

***

## Model Development

Use 2 classifier architecture:
- 1 model generates labels
- 1 model classifies all training data

Model 1:
- Train on songs with only one artist and one genre (L)
- Generate a genre for artists that don't have any genre. (U)
- Find the most likely genre for songs with more than one artist/genre. (U)

Model 2: Classification Model (IDK just pick one)
- Train on training subset of L, all unlabeled data U.
- Use micro-averaged ROC curve to assess model performance.

***











