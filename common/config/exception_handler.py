from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.main import app
from common.config.exception import NotFoundException
from common.config.logger import logger


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc):
    logger.error(f"NotFoundException: {exc.detail}")
    return JSONResponse(
        status_code=404,
        content={"message": str(exc.detail), "error": "NOT_FOUND"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail), "error": "HTTPException"},
    )
