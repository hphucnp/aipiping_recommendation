from beanie import init_beanie
from fastapi import FastAPI

from app.api.v1.recommendation import router as recommendations_router
from common.config.client.mongo_client import mongo_client
from common.model.recommendation import Recommendation

app = FastAPI()

app.include_router(recommendations_router)


async def init():
    await init_beanie(database=mongo_client.recommendations, document_models=[Recommendation])


@app.on_event("startup")
async def startup_event():
    await init()


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
