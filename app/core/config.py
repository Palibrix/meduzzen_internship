import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
	host = os.environ.get("HOST")
	port = int(os.environ.get("WEB_PORT"))
	reload = bool(os.environ.get("RELOAD"))
