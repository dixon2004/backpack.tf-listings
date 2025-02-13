from dotenv import load_dotenv
import os

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL")
LISTINGS_MANAGER_URL = os.getenv("LISTINGS_MANAGER_URL")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
SAVE_USER_DATA = os.getenv("SAVE_USER_DATA", "false").lower() == "true"
WS_MANAGER_URL = os.getenv("WS_MANAGER_URL")
