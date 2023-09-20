from aio_pika import connect, Message, DeliveryMode
import json


class Rabbit_MQ:
    default_url = "amqp://guest:guest@localhost/"
    connection = []
    @staticmethod
    async def connect_broker(url:str = default_url):


        ...
    

    @staticmethod
    async def publish_message(message:dict):
        message_body = json.dumps(message)
        message = Message(body=b'message_body', delivery_mode=DeliveryMode.PERSISTENT)
        
        ...