from database.listings import ListingsDatabase
from utils.logger import SyncLogger
from utils.utils import tf2
import time


cache_database = {}


class CacheService:

    def __init__(self) -> None:
        """
        Initialize the CacheService class.
        """
        self.logger = SyncLogger("CacheService")
        self.db = ListingsDatabase()


    async def check_item_exists(self, item_name: str) -> bool:
        """
        Check if the item exists in the cache or the database.

        Args:
            item_name (str): Name of the item.

        Returns:
            bool: True if the item exists, False otherwise.
        """
        current_time = time.time()

        if (
            not cache_database 
            or not cache_database.get("last_update")
            or (current_time - cache_database["last_update"]) > 1800
        ):
            await self.refresh_cache()

        return item_name in cache_database.get("items", {})


    async def refresh_cache(self) -> None:
        """
        Refresh the cache with items in the database.
        """
        global cache_database
        db_collections = await self.db.get_collections()

        items = {
            tf2.get_name_from_sku(item_sku): item_sku 
            for item_sku in db_collections
        }

        cache_database = {
            "last_update": time.time(),
            "items": items
        }

        self.logger.write_log("info", f"Successfully refreshed cache with {len(items)} items")


    def add_item(self, item_sku: str) -> None:
        """
        Add item to the cache.

        Args:
            item_sku (str): SKU of the item.
        """
        global cache_database

        if "items" not in cache_database:
            cache_database["items"] = {}

        if item_sku not in cache_database["items"].values():
            item_name = tf2.get_name_from_sku(item_sku)
            cache_database["items"][item_name] = item_sku
            self.logger.write_log("info", f"Added item to cache: {item_name}")


    def get_sku_from_name(self, item_name: str) -> str:
        """
        Convert item name to item SKU from the cache.

        Args:
            item_name (str): Name of the item.

        Returns:
            str: The SKU of the item if found, otherwise None.
        """
        return cache_database["items"].get(item_name, None)
