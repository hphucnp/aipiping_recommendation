from typing import List
from uuid import uuid4

from common.config.exception import NotFoundException
from common.model.common import IdModel
from common.model.recommendation import Recommendation


class RecommendationService:
    'Central service for CRUD operations'
    @staticmethod
    async def save(data) -> IdModel:
        'Save recommendation into mongo db and return the id immediately'
        uid = str(uuid4())
        recommendation = Recommendation.model_validate({**data, "id": str(uid)})
        await recommendation.insert()
        return IdModel(id=uid)

    @staticmethod
    async def get(uid) -> Recommendation:
        'Get a single recommendation'
        recommendation = await Recommendation.get(document_id=uid)
        if not recommendation:
            raise NotFoundException(detail=f"Recommendation {uid} not found")
        return recommendation

    @staticmethod
    async def query() -> List[Recommendation]:
        'Get list of recommendations'
        return await Recommendation.find({}).to_list()


recommendationService = RecommendationService()
