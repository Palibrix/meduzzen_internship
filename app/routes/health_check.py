from fastapi import APIRouter, Depends, HTTPException
from redis import asyncio as aioredis
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.db.database import get_session
from app.services.redis import rd

router = APIRouter()


@router.get('/')
def index():
    return JSONResponse(content={
        "status_code": 200, "detail": "ok", "result": "working"
                        })


@router.get("/test_redis_connection")
async def test_redis_connection():
    try:
        await rd.ping()
        return JSONResponse(content={
            "message": "Redis connection is successful!"
                            })
    except aioredis.RedisError as e:
        return JSONResponse(content={
            "message": f"Redis connection failed: {str(e)}"
                            })


@router.get("/test_db_connection")
async def test_db_connection(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(text('SELECT 1'))
        return {
            "status": "success",
            "result": result.scalar_one()
        }
    except OperationalError:
        raise HTTPException(status_code=500,
                            detail="Failed to connect to the database.q")
