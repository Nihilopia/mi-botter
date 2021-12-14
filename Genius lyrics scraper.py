# Genius lyrics scraper
import os
import requests
from googleapiclient.discovery import build

# Genius API access token
# genius_token = os.environ["geniustoken"]
google_token = os.environ["googlesearchtoken"]

# search_endpoint = f"https://www.googleapis.com/customsearch/v1?q={searchTerms}searchType={searchType}&alt=json"


def google_search(query):
    service = build("customsearch", "v1", developerKey=google_token)
    res = service.cse().list(q=query, cx="0b4ae830bfb628304").execute()
    
    links = []
    for result in res["items"]:
        links.append(result["link"])

    return links

def curl_lyrics(url):
    req = requests.get(url)
    return req.text.replace("\\n", "\n")

def parse_lyrics_html(html):
    # TODO
    pass


results = google_search('Haftbefehl - Ballermann' + ' lyrics genius.com')
res1 = curl_lyrics(results[0])
pass