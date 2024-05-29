import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(verbose=True)


class Settings(BaseSettings):
    MONGODB_URI: str = os.environ.get("MONGODB_URI", "mongodb://mongo:27017")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    KAFKA_BOOTSTRAP_SERVER: str = os.environ.get("KAFKA_BOOTSTRAP_SERVER", 'kafka:9092')
    KAFKA_WORKER_TOPIC: str = os.environ.get("KAFKA_WORKER_TOPIC", "JUST_DO_IT")


settings = Settings()
