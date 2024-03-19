import requests
from utils.logger import Logger

logger = Logger("shazam.api.log")


def recognition(file_name):
    url = "https://shazam-api-free.p.rapidapi.com/shazam/recognize/"

    headers = {
        "X-RapidAPI-Key": "cd43af9cfdmsh6c224a18db2e7d9p182ab9jsneb1b946a7f1b",
        "X-RapidAPI-Host": "shazam-api-free.p.rapidapi.com"
    }

    file_path = f'./downloads/{file_name}.mp3'
    with open(file_path, 'rb') as f:
        files = {'upload_file': (f'{file_path}', f, 'audio/mpeg')}
        response = requests.post(url, files=files, headers=headers)

    title = response.json()['track']['title']
    artist = response.json()['track']['subtitle']
    logger.info(f"Recognized song: {title} | {artist}")
    return title, artist
