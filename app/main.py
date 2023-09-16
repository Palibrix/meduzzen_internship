import uvicorn

from fastapi import FastAPI

from app.core.config import HOST, PORT, RELOAD
from app.routes import health_check

app = FastAPI()

app.include_router(health_check.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=RELOAD)
