from typing import Union

from fastapi import FastAPI
from app.api.v1.recommendations import router as recommendations_router

app = FastAPI()

app.include_router(recommendations_router)

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
