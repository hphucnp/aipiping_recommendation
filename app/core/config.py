from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI: str = Field("mongodb://mongo:27017", env="MONGODB_URI")
    OPENAI_API_KEY: str = Field(env="OPENAI_API_KEY")


settings = Settings()
