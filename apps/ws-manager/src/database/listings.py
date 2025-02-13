from utils.config import DATABASE_URL
from utils.logger import SyncLogger
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL, minPoolSize=10, maxPoolSize=200)


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


    async def update(self, sku: str, listings: list) -> None:
        """
        Update listings in the database.
        
        Args:
            sku (str): SKU of the item.
            listings (list): List of listings.
        """
        try:
            await self.db[sku].update_one({"_id": listings["_id"]}, {"$set": listings}, upsert=True)
        except Exception as e:
            self.logger.write_log("error", f"Failed to update listings: {e}")


    async def delete(self, sku: str, id: str) -> None:
        """
        Delete listing from the database.
        
        Args:
            sku (str): SKU of the item.
            id (str): ID of the listing.
        """
        try:
            await self.db[sku].delete_one({"_id": id})
        except Exception as e:
            self.logger.write_log("error", f"Failed to delete listing: {e}")
