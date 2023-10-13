from typing import ClassVar

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    host: str
    port: int
    reload: bool

    db_url: str

    redis_port: int
    redis_host: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    audience: str

    pwd_context: ClassVar = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme: ClassVar = OAuth2PasswordBearer(tokenUrl="token")

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = ServerSettings()
