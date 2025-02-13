from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SAVE_USER_DATA = os.getenv("SAVE_USER_DATA", "false").lower() == "true"
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
