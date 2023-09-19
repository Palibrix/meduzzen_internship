from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    host: str
    port: int
    reload: bool

    model_config = SettingsConfigDict(env_file=".env")
