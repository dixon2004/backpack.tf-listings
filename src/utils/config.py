from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BPTF_TOKEN = os.getenv("BPTF_TOKEN", "").split(",")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
SAVE_USER_DATA = os.getenv("SAVE_USER_DATA", "false").lower() == "true"
SERVER_PORT = int(os.getenv("SERVER_PORT", 3000))
