from dotenv import load_dotenv
import os

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
WS_MANAGER_URL = os.getenv("WS_MANAGER_URL")
BPTF_TOKEN = [token.strip() for token in list(os.getenv("BPTF_TOKEN", "").split(","))]
DATABASE_URL = os.getenv("DATABASE_URL")
