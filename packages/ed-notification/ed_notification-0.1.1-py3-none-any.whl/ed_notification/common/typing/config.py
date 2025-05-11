from typing import TypedDict


class RabbitMQConfig(TypedDict):
    url: str
    queue: str


class Config(TypedDict):
    resend_api_key: str
    infobig_key: str
    mongo_db_connection_string: str
    db_name: str
    rabbitmq: RabbitMQConfig


class TestMessage(TypedDict):
    title: str
