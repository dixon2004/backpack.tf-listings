from database.listings import ListingsDatabase
from api.ws_manager import WebsocketManager
from api.backpack_tf import BackpackTFAPI
from utils.logger import SyncLogger
import asyncio
import random


class ListingsUpdater:

    def __init__(self) -> None:
        """
        Initialize the ListingsUpdater class.
        """
        self.logger = SyncLogger("ListingsUpdater")
        self.listings_db = ListingsDatabase()
        self.ws_manager = WebsocketManager()
        self.bptf = BackpackTFAPI()


    async def run(self) -> None:
        """
        Run the listings update process.
        """
        while True:
            try:
                collections = await self.listings_db.get_collections()
                items_count = len(collections)
                if not items_count:
                    self.logger.write_log("info", "No items found in the database")
                    await asyncio.sleep(60)
                    continue

                sleep_time = 1 if items_count < 1000 else 0.5

                random.shuffle(collections)

                self.logger.write_log("info", f"Starting listings update process for {len(collections)} items")
                for sku in collections:
                    try:
                        listings = await self.bptf.get_listings(sku)
                        if not listings:
                            raise Exception("No listings found.")
                        
                        await self.ws_manager.remove_updates_from_queue(sku)

                        item_name = listings[0]["name"]
                        self.logger.write_log("info", f"Successfully updated listings for {item_name} ({sku})")

                    except Exception as e:
                        self.logger.write_log("error", f"Failed to update listings for {sku}: {e}")

                    await asyncio.sleep(sleep_time)
                
                self.logger.write_log("info", "All listings updated successfully")
            except Exception as e:
                self.logger.write_log("error", f"Critical error during the update process: {e}")

            self.logger.write_log("info", "Pausing updates for 60 seconds")
            await asyncio.sleep(60)
