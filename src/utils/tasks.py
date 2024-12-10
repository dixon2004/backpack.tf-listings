from data.database import ListingsDatabase
from api.backpack_tf import BackpackTFAPI
from utils.logger import SyncLogger
import asyncio
import random


class BackgroundTasks:

    def __init__(self) -> None:
        """
        Initialize the BackgroundTasks class.
        """
        self.logger = SyncLogger("BackgroundTasks")
        self.bptf = BackpackTFAPI()
        self.listings_db = ListingsDatabase()


    async def refresh_listings(self) -> None:
        """
        Refresh listings in the database.
        """
        while True:
            try:
                collections = await self.listings_db.get_collections()
                random.shuffle(collections)
                for sku in collections:
                    try:
                        listings = await self.bptf.get_listings(sku)
                        if not listings:
                            raise Exception("Listings not found.")
                        
                        item_name = listings[0]["name"]
                        self.logger.write_log("info", f"Refreshing listings: {item_name}")
                    except Exception as e:
                        self.logger.write_log("error", f"Failed to refresh listings ({sku}): {e}")
                    await asyncio.sleep(1)
            except Exception as e:
                self.logger.write_log("error", f"Failed to refresh listings in background: {e}")
            await asyncio.sleep(60)
