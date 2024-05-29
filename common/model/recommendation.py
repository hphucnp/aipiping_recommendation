from enum import Enum
from typing import List, Optional

from beanie import Document
from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field


class RecommendationStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Season(str, Enum):
    SUMMER = "summer"
    WINTER = "winter"
    SPRING = "spring"
    AUTUMN = "autumn"


# Define the document model
class Recommendation(Document):
    'Main model for Recommendation'
    id: Optional[str] = Field(alias="_id")
    country: str
    season: Season
    recommendations: List[str]
    status: RecommendationStatus

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }


# Define the response model for pending recommendation
class PendingRecommendationResponse(BaseModel):
    id: str
    status: RecommendationStatus
    message: str

class RecommendationResponse(BaseModel):
    id: str
    country: str
    season: Season
    recommendations: List[str]
    status: RecommendationStatus
