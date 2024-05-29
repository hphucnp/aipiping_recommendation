from enum import Enum
from typing import List

from beanie import init_beanie, Document
from pydantic import Field
import asyncio
import openai
from pymongo import MongoClient

from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

client = MongoClient(settings.MONGODB_URI)
db = client.travel_recommendations
collection = db.recommendations




# Establish a connection to the MongoDB server
client = MongoClient(settings.MONGODB_URI)

async def init():
    # Initialize Beanie with the database and the document model
    await init_beanie(database=client.test, document_models=[Recommendation])

# Call the init function
asyncio.run(init())


def fetch_recommendations(country: str, season: str):
    response = openai.Completion.create(
        model=settings.OPENAI_MODEL,
        prompt=f"Give me three recommendations of things to do in {country} during {season}.",
        max_tokens=100,
    )
    return response.choices[0].text.strip().split("\n")
