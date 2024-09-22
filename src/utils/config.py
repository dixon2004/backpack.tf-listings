from dotenv import load_dotenv
import json
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BPTF_TOKEN = os.getenv("BPTF_TOKEN").split(",")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

options_template = {
    "save_user_data": False,
    "auth_token": "",
    "port": 8000
}
options_path = "./options.json"

if not os.path.exists(options_path):
    with open(options_path, "w") as f:
        json.dump(options_template, f, indent=4)

with open(options_path, "r") as f:
    options = json.load(f)

save_user_data = options.get("save_user_data", False)
