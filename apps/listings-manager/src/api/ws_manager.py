from utils.config import WS_MANAGER_URL
from utils.logger import SyncLogger
import aiohttp


class WebsocketManager:

    def __init__(self) -> None:
        """
        Initialize the WebsocketManager class.
        """
        self.url = WS_MANAGER_URL
        self.logger = SyncLogger("WebsocketManager")


    async def remove_updates_from_queue(self, sku: str) -> None:
        """
        Remove updates from listing updates queue.
        
        Args:
            sku (str): SKU of the item.
        """
        try:
            data = {"item_sku": sku}
            async with aiohttp.ClientSession() as session:
                async with session.delete(f"{self.url}/queue", json=data, timeout=10) as response:
                    response.raise_for_status()
        except Exception as e:
            self.logger.write_log("error", f"Failed to remove updates from the queue: {e}")


    async def add_item_to_cache(self, sku: str) -> None:
        """
        Add an item to item cache.
        
        Args:
            sku (str): SKU of the item.
        """
        try:
            data = {"item_sku": sku}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.url}/item", json=data, timeout=10) as response:
                    response.raise_for_status()
        except Exception as e:
            self.logger.write_log("error", f"Failed to add item to the cache: {e}")
