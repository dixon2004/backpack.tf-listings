from utils.config import STEAM_API_KEY
from tf2utilities.main import TF2

tf2 = TF2(STEAM_API_KEY, auto_update=True).schema
