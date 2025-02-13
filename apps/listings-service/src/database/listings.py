from utils.config import DATABASE_URL
from utils.logger import SyncLogger
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)


class ListingsDatabase:

    def __init__(self) -> None:
        """
        Initialize the Backpack.tf listings database.
        """
        self.db = client["backpacktf_listings"]
        self.logger = SyncLogger("ListingsDatabase")


    async def get_collections(self) -> list:
        """
        Get collections from the database.
        
        Returns:
            list: List of collections.
        """
        try:
            return await self.db.list_collection_names()
        except Exception as e:
            self.logger.write_log("error", f"Failed to get collections: {e}")


    async def get(self, sku: str) -> list:
        """
        Get listings from the database.
        
        Args:
            sku (str): SKU of the item.
            
        Returns:
            list: List of listings.
        """
        try:
            cursor = self.db[sku].find({}, {"_id": False})
            return await cursor.to_list(length=None)
        except Exception as e:
            self.logger.write_log("error", f"Failed to get listings: {e}")


    async def delete_all(self, sku: str) -> None:
        """
        Delete all listings from the database.
        
        Args:
            sku (str): SKU of the item.
        """
        try:
            await self.db[sku].delete_many({})
        except Exception as e:
            self.logger.write_log("error", f"Failed to delete all listings: {e}")
