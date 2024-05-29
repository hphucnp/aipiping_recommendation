import time
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.db.mongo import collection
from prefect import task, flow, Flow
prefect.


router = APIRouter()


class RequestRecommendation(BaseModel):
    country: str
    season: str


# Define a Prefect task
@task
def process_recommendation(uid):
    time.sleep(10)
    # This is where you would put the code to process the recommendation
    print(f"Processing recommendation with UID {uid}")


@router.post("/recommendations")
def request_recommendations(country: str = Query(), season: str = Query()):
    if season.lower() not in ["summer", "winter", "spring", "autumn"]:
        raise HTTPException(status_code=400, detail="Invalid season")

    uid = str(uuid4())

    @flow
    async def execute_flow():
        process_recommendation(uid)
    # Create a new Prefect flow
    execute_flow()

    # Run the flow in the background

    return {"uid": uid}


@router.get("/recommendations/{uid}")
def get_recommendations(uid: str):
    recommendation = collection.find_one({"uid": uid})
    if not recommendation:
        raise HTTPException(status_code=404, detail="UID not found")

    return recommendation
