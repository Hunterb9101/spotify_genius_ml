import requests
import json
import pandas as pd

with open("keys.json") as f:
    KEYS = json.load(f)

headers = {
    "Ocp-Apim-Subscription-Key": KEYS["AZURE_API_ID"],
    "Ocp-Apim-Subscription-Region": KEYS["AZURE_API_REGION"],

}

params = {
    "to": "en",
    "Content-type": "application/json",
    "api-version": "3.0"
}

df = pd.read_csv("data/raw/lyrics_to_translate.csv")["lyrics"].tolist()

text = ["hola"]
body = [{"text": x} for x in text]

r = requests.post('https://api.cognitive.microsofttranslator.com/translate', headers=headers, params=params, json=body)
print(json.dumps(r.json(), sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
