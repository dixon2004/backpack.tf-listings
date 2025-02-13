from utils.config import LISTINGS_MANAGER_URL
from utils.logger import SyncLogger
import aiohttp


class ListingsManager:

    def __init__(self) -> None:
        """
        Initialize the ListingsManager class.
        """
        self.url = LISTINGS_MANAGER_URL
        self.logger = SyncLogger("ListingsManager")


    async def get_listings(self, sku: str) -> list:
        """
        Get item listings from the listings manager.
        
        Args:
            sku (str): SKU of the item.

        Returns:
            list: List of item listings.
        """
        try:
            params = {"item_sku": sku}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.url}/listings", params=params, timeout=10) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            self.logger.write_log("error", f"Failed to get listings: {e}")
