# Define the status enum
from enum import Enum
from typing import List

from beanie import init_beanie, Document
from pydantic import Field


class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


# Define the document model
class Recommendation(Document):
    id: str = Field(..., alias="_id")
    country: str
    season: str
    recommendations: List[str]
    status: Status
