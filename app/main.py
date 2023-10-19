import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import health_check, user_routes, authentication_routes, company_routes, action_routes, quiz_routes

app = FastAPI()

app.include_router(health_check.router, tags=["Health"])
app.include_router(user_routes.router, tags=["User"])
app.include_router(authentication_routes.router, tags=["Authentication"])
app.include_router(company_routes.router, tags=["Company"])
app.include_router(action_routes.router, tags=["Action"])
app.include_router(quiz_routes.router, tags=["Quiz"])

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.host,
                port=settings.port, reload=settings.reload)
