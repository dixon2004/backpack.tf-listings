from data.database import ListingsDatabase
from api.backpack_tf import BackpackTFAPI
from utils.log import write_log
import asyncio
import random


class BackgroundTasks:

    def __init__(self) -> None:
        self.bptf = BackpackTFAPI()
        self.listings_db = ListingsDatabase()


    async def refresh_listings(self) -> None:
        """
        Refresh listings in the database.
        """
        try:
            collections = await self.listings_db.get_collections()
            random.shuffle(collections)
            for sku in collections:
                try:
                    listings = await self.bptf.get_listings(sku)
                    if not listings:
                        raise Exception("Listings not found.")
                    
                    item_name = listings[0]["name"]
                    write_log("info", f"[BackgroundTasks] Refreshed listings: {item_name}")
                except Exception as e:
                    write_log("error", f"[BackgroundTasks] Failed to refresh listings ({sku}): {e}")
                await asyncio.sleep(1)
        except Exception as e:
            write_log("error", f"[BackgroundTasks] Failed to refresh listings in background: {e}")
