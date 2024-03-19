import time

import requests

from mailgun.send_email import send_simple_message
from db.configs import POSTGRESQL_URL
from db.connection import Connection
from db.queries import CHECK_ANY_READY, UPDATE_STATUS
from utils.logger import Logger

logger = Logger("main.log")


def process_ready_request(connection):
    while True:
        time.sleep(5)
        if connection.open():
            res = connection.execute_query(CHECK_ANY_READY)
            for record in res:
                record_id = record[0]
                email = record[1]
                song_id = record[3]

                url = "https://spotify23.p.rapidapi.com/recommendations/"

                querystring = {"limit": "5", "seed_tracks": song_id}

                headers = {
                    "X-RapidAPI-Key": "cd43af9cfdmsh6c224a18db2e7d9p182ab9jsneb1b946a7f1b",
                    "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
                }

                response = requests.get(url, headers=headers, params=querystring)
                similars = response.json()['tracks']
                res = []
                for similar in similars:
                    artists = [artist['name'] for artist in similar['artists']]
                    name = similar['name']
                    url = similar['external_urls']['spotify']
                    res.append((artists, name, url))
                send_simple_message(email, res)
                connection.execute_query(UPDATE_STATUS, (record_id, ))
                logger.info(f"Sent email: {res}")


if __name__ == "__main__":
    connection = Connection(POSTGRESQL_URL)
    process_ready_request(connection)
