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


    async def get(self, steam_id: str) -> dict:
        """
        Get user from the database.
        
        Args:
            steam_id (str): Steam ID of the user.
            
        Returns:
            dict: User data.
        """
        try:
            return await self.collection.find_one({"_id": steam_id}, {"_id": False})
        except Exception as e:
            self.logger.write_log("error", f"Failed to get user: {e}")


    async def drop_database(self) -> None:
        """
        Drop the users collection.
        """
        try:
            await self.collection.drop()
        except Exception as e:
            self.logger.write_log("error", f"Failed to drop database: {e}")
