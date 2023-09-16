import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes import health_check

load_dotenv()
HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))
RELOAD = bool(os.environ.get("RELOAD"))
app = FastAPI()

app.include_router(health_check.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=RELOAD)
