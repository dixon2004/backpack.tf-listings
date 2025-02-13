from database.listings import client
from utils.logger import SyncLogger


class UsersDatabase:

    def __init__(self) -> None:
        """
        Initialize the users database.
        """
        self.db = client["backpacktf_users"]
        self.collection = self.db["users"]
        self.logger = SyncLogger("UsersDatabase")


    async def insert(self, user: dict) -> None:
        """
        Insert user into the database.
        
        Args:
            user (dict): User data.
        """
        try:
            await self.collection.update_one({"_id": user["id"]}, {"$set": user}, upsert=True)
        except Exception as e:
            self.logger.write_log("error", f"Failed to insert user: {e}")
