from utils.config import DATABASE_URL
from utils.logger import AsyncLogger
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL, maxPoolSize=200, minPoolSize=10)


class ListingsDatabase:

    def __init__(self) -> None:
        """
        Initialize the Backpack.tf listings database.
        """
        self.logger = AsyncLogger("ListingsDatabase")
        self.db = client["backpacktf_listings"]


    async def get_collections(self) -> list:
        """
        Get collections from the database.
        
        Returns:
            list: List of collections.
        """
        try:
            return await self.db.list_collection_names()
        except Exception as e:
            await self.logger.write_log("error", f"Failed to get collections: {e}")


    async def check_collection(self, sku: str) -> bool:
        """
        Check if the collection exists in the database.
        
        Args:
            sku (str): SKU of the item.
            
        Returns:
            bool: True if the collection exists, False otherwise.
        """
        try:
            return sku in await self.get_collections()
        except Exception as e:
            await self.logger.write_log("error", f"Failed to check collection: {e}")


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
            await self.logger.write_log("error", f"Failed to get listings: {e}")


    async def insert(self, sku: str, listings: list) -> None:
        """
        Insert listings into the database.
        
        Args:
            sku (str): SKU of the item.
            listings (list): List of listings.
        """
        try:
            await self.db[sku].insert_many(listings)
        except Exception as e:
            await self.logger.write_log("error", f"Failed to insert listings: {e}")


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
            await self.logger.write_log("error", f"Failed to update listings: {e}")


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
            await self.logger.write_log("error", f"Failed to delete listing: {e}")


    async def delete_all(self, sku: str) -> None:
        """
        Delete all listings from the database.
        
        Args:
            sku (str): SKU of the item.
        """
        try:
            await self.db[sku].delete_many({})
        except Exception as e:
            await self.logger.write_log("error", f"Failed to delete all listings: {e}")


class UsersDatabase:

    def __init__(self) -> None:
        """
        Initialize the users database.
        """
        self.logger = AsyncLogger("UsersDatabase")
        self.db = client["backpacktf_users"]
        self.collection = self.db["users"]


    async def insert(self, user: dict) -> None:
        """
        Insert user into the database.
        
        Args:
            user (dict): User data.
        """
        try:
            await self.collection.update_one({"_id": user["id"]}, {"$set": user}, upsert=True)
        except Exception as e:
            await self.logger.write_log("error", f"Failed to insert user: {e}")

        
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
            await self.logger.write_log("error", f"Failed to get user: {e}")


    async def drop_database(self) -> None:
        """
        Drop the users collection.
        """
        try:
            await self.collection.drop()
        except Exception as e:
            await self.logger.write_log("error", f"Failed to drop database: {e}")
