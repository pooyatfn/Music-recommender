import pika

from db.configs import *
from db.connection import Connection
from db.queries import *
from object_storage.downloader import download_file
from shazam.api import recognition
from spotify.search import search_music
from utils.logger import Logger

logger = Logger("queue_reader.log")
postgresql = Connection(POSTGRESQL_URL)
RABBITMQ_URL = os.getenv("RABBITMQ_URL",
                         "amqps://boobhhqt:EXdgXbDHAA60dD9DhLw4ZUA7_nzqW7tX@rat.rmq2.cloudamqp.com/boobhhqt")


def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    request_id = body.decode()
    logger.info(f"Received id {request_id} from rabbitMQ")
    download_file(request_id, request_id)
    title, artist = recognition(request_id)
    song_id = search_music(title + " " + artist)

    if not postgresql.open():
        return
    params = (song_id, request_id)
    try:
        postgresql.execute_query(UPDATE_SONG_ID, params)
        postgresql.close()
    except Exception as e:
        logger.error(f"Updating data to postgres failed: {e}")
        return


def start_consuming():
    params = pika.URLParameters(RABBITMQ_URL)
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
    except Exception as e:
        logger.error(f"Could not connect to rabbitMQ: {e}")
        return

    channel.queue_declare(queue='ids')
    logger.info('Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='ids', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    start_consuming()
