import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures

songs = pd.read_csv(f"data/rematch_raw/lyrics_join.csv").to_dict(orient="records")


def lyrics_from_path(path):
    # gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    # remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    # at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_="lyrics").get_text()  # updated css where the lyrics are based in HTML
    return lyrics


def gen_lyrics_chunk(i):
    print(f"Starting chunk {i}")
    lyrics = []
    ub = i*1000
    if ub > len(songs):
        ub = len(songs)
    for s in songs[(i-1)*1000: ub]:
        errors = 0
        while errors < 3:
            try:
                t = s
                t["lyrics"] = lyrics_from_path(s['lyrics_path'])
                lyrics.append(t)
                break
            except AttributeError:
                #print(f"Error on chunk {i}: {s['lyrics_path']}")
                errors += 1
    pd.DataFrame(lyrics).to_csv(f"data/rematch_raw/lyrics/lyrics_part{i:.0f}.csv")
    return i


with concurrent.futures.ThreadPoolExecutor(max_workers=48) as executor:
    future_to_lyrics = {executor.submit(gen_lyrics_chunk, i) for i in range(1, int(len(songs)/1000)+1)}
    for future in concurrent.futures.as_completed(future_to_lyrics):
        print(f"Finished chunk {future.result()}")
