import uvicorn

from fastapi import FastAPI

from app.core.config import Settings
from app.routes import health_check

app = FastAPI()
settings = Settings()

app.include_router(health_check.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.reload)
