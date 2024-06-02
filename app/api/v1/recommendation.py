from typing import List, Union

from confluent_kafka import Producer
from fastapi import APIRouter, Query

from common.config.logger import logger
from common.config.settings import settings
from common.model.common import IdModel
from common.model.recommendation import (
    PendingRecommendationResponse, RecommendationResponse, RecommendationStatus, Season
)
from common.service.recommendation import recommendationService

router = APIRouter()

kafka_producer = Producer({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVER})
KAFKA_TOPIC = settings.KAFKA_WORKER_TOPIC


@router.post("/recommendations/create")
async def create_recommendation(country: str = Query(), season: Season = Query()) -> IdModel:
    'Save the request for recommendation to the database'
    logger.info("Requesting recommendations for %s during %s", country, season.value)
    data = {
        "country": country,
        "season": season,
        "recommendations": [],
        "status": RecommendationStatus.PENDING
    }
    response = await recommendationService.save(data)

    kafka_producer.produce(KAFKA_TOPIC, key=response.id, value=response.id)

    return response


@router.post("/recommendations/{uid}/get")
async def get_recommendation(uid: str) -> Union[RecommendationResponse, PendingRecommendationResponse]:
    'Get detail of one recommendation request'
    logger.info("Get recommendation with uid: %s", uid)
    recommendation = await recommendationService.get(uid)
    if recommendation.status == RecommendationStatus.PENDING:
        return PendingRecommendationResponse(**{
            "id": recommendation.id,
            "status": RecommendationStatus.PENDING,
            "message": "The recommendation is not yet available. Please try again later."
        })
    return RecommendationResponse(**recommendation.model_dump())


@router.post("/recommendations/query")
async def get_recommendations() -> List[RecommendationResponse]:
    'Get all recommendations out of database, for testing only'
    logger.info("Get all recommendations")
    return [RecommendationResponse(**rem.model_dump())
            for rem in (await recommendationService.query())]
