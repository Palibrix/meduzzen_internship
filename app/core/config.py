from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    host: str
    port: int
    reload: bool

    db_url: str

    redis_port: int
    redis_host: str

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = ServerSettings()
