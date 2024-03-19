import requests
from utils.logger import Logger

logger = Logger("spotify.search.log")

url = "https://spotify23.p.rapidapi.com/search/"


def search_music(keyword):
    querystring = {"q": f"{keyword}", "type": "tracks", "offset": "0", "limit": "1",
                   "numberOfTopResults": "1"}

    headers = {
        "X-RapidAPI-Key": "cd43af9cfdmsh6c224a18db2e7d9p182ab9jsneb1b946a7f1b",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    song_id = response.json()['tracks']['items'][0]['data']['id']
    logger.info(response.json()['tracks']['items'][0]['data'])

    return song_id
