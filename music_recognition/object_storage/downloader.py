import boto3

from object_storage.configs import *
from utils.logger import Logger

logger = Logger("object_storage.downloader.log")

s3 = boto3.client(
    "s3",
    endpoint_url=OBJECT_STORAGE_ENDPOINT,
    aws_access_key_id=OBJECT_STORAGE_ACCESS_KEY,
    aws_secret_access_key=OBJECT_STORAGE_SECRET_KEY,
)


def download_file(filename_in_system, filename_in_bucket):
    file_path = './downloads/' + filename_in_system + '.mp3'
    s3.download_file(OBJECT_STORAGE_BUCKET_NAME, filename_in_bucket, file_path)
    logger.info(f"File with name {filename_in_bucket}, was downloaded in system as {filename_in_system}")
