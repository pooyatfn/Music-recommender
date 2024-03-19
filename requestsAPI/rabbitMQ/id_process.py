import pika
from rabbitMQ.configs import *
from utils.logger import Logger

logger = Logger("rabbitMQ.id_process.log")

params = pika.URLParameters(RABBITMQ_URL)


def send_id(request_id: int):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='ids')
    properties = pika.BasicProperties(correlation_id='my_unique_id')
    channel.basic_publish(exchange='', routing_key='ids', body=request_id, properties=properties)
    logger.info(f"ID {request_id} was inserted")

    connection.close()
