import os

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

DATABASE_URI = os.getenv("DATABASE_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")