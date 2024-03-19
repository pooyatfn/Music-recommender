import boto3

from object_storage.configs import *
from utils.logger import Logger

logger = Logger("object_storage.uploader.log")

s3 = boto3.client(
    "s3",
    endpoint_url=OBJECT_STORAGE_ENDPOINT,
    aws_access_key_id=OBJECT_STORAGE_ACCESS_KEY,
    aws_secret_access_key=OBJECT_STORAGE_SECRET_KEY,
)


def upload_file(file, key):
    s3.upload_fileobj(file, OBJECT_STORAGE_BUCKET_NAME, key)
    logger.info(f"File with name {key}, was uploaded")
