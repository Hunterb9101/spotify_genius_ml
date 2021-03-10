from data_collection_old.oauth import OAuth
import pandas as pd
import transform_util
from datetime import datetime as dt
import json
# Started at 2:40 PM

start = dt.now()
with open("keys.json") as f:
    KEYS = json.load(f)

genius = OAuth(client_id=KEYS["GENIUS_API_ID"],
               client_secret=KEYS["GENIUS_API_SECRET"],
               access_token_url='https://api.genius.com/oauth/token',
               authorize_url='https://api.genius.com/oauth/authorize',
               base_url='https://api.genius.com/')

songs = pd.read_csv("../data/pre_raw/rnd1_songs.csv")
songs['artists'] = songs['artists'].apply(lambda x: transform_util.str_to_list(x))


song_titles = songs[['name', 'cleaned_name', 'artists', 'id']].to_dict(orient='records')
song_lyrics = []
skip_to = 162001
for i, s in enumerate(song_titles):
    if i < skip_to:
        continue
    print(f"{i}: {s['name']} by {s['artists']}")
    if i % 1000 == 0:
        pd.DataFrame(song_lyrics).to_csv(f"data/pre_raw/matching_rnd1/lyrics_part_{i/1000:.0f}.csv", index=False)
        song_lyrics = []

    params = {'q': s['name']}
    rest_results = genius.session.get('search', params=params).json()

    if len(rest_results['response']['hits']) == 0:
        continue

    results = rest_results['response']['hits']
    artists_fmt = s['artists']
    found_record = None
    """
    Lyric/Song Matching:
    3 rules to get matched:
     - Exact title and primary artist match (Highest confidence)
     - Exact title match
     - Only search result (Lowest confidence)
     
    All search results are assumed to be in order of relevance, and the highest confidence result is given. 
    """
    for r in results:
        # Exact title/artist match
        if r['type'] == 'song' and r['result']['primary_artist']['name'] in artists_fmt \
                and r['result']['title'] == s['cleaned_name']:
            if found_record is None or found_record['lyric_confidence'] < 3:
                found_record = r['result']
                found_record['spotify_id'] = s['id']
                found_record['lyric_confidence'] = 3
        # Exact title match
        elif r['type'] == 'song' and r['result']['title'] == s['cleaned_name']:
            if found_record is None or found_record['lyric_confidence'] < 2:
                found_record = r['result']
                found_record['spotify_id'] = s['id']
                found_record['lyric_confidence'] = 2
        # Only search result
        elif r['type'] == 'song' and len(results) == 1:
            if found_record is None:
                found_record = r['result']
                found_record['spotify_id'] = s['id']
                found_record['lyric_confidence'] = 1
    if found_record is not None:
        song_lyrics.append(found_record)

pd.DataFrame(song_lyrics).to_csv("data/intermediate/matching_rnd1/lyrics_end.csv", index=False)
end = dt.now()
print(f"Took: {(start-end).total_seconds()} seconds")