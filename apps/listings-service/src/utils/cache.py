from database.listings import ListingsDatabase
from utils.logger import SyncLogger
import time


class CacheService:

    def __init__(self) -> None:
        """
        Initialize the CacheService class.
        """
        self.cache = []
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
            not self.cache 
            or not self.cache.get("last_update")
            or (current_time - self.cache["last_update"]) > 1800
        ):
            await self.refresh_cache()

        return item_name in self.cache.get("items", set())


    async def refresh_cache(self) -> None:
        """
        Refresh the cache with items in the database.
        """
        items = await self.db.get_collections()
        self.cache = {
            "last_update": time.time(),
            "items": set(items)
        }
        self.logger.write_log("info", f"Successfully refreshed cache with {len(items)} items")


    def add_item(self, item_sku: str) -> None:
        """
        Add item to the cache.

        Args:
            item_sku (str): SKU of the item.
        """
        if "items" not in self.cache:
            self.cache["items"] = set()

        self.cache["items"].add(item_sku)
        self.logger.write_log("info", f"Added item to cache: {item_sku}")


    def remove_item(self, item_sku: str) -> None:
        """
        Remove item from the cache.

        Args:
            item_sku (str): SKU of the item.
        """
        if "items" in self.cache:
            self.cache["items"].remove(item_sku)
            self.logger.write_log("info", f"Removed item from cache: {item_sku}")
