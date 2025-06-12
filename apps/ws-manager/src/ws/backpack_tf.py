from database.listings import ListingsDatabase
from utils.queue import ListingsQueueService
from utils.utils import tf2, get_spell_id
from database.users import UsersDatabase
from utils.config import SAVE_USER_DATA
from utils.cache import CacheService
from utils.logger import SyncLogger
import websockets
import asyncio
import orjson
import time
import math


class BackpackTFWebSocket:

    def __init__(self) -> None:
        """
        Initialize the BackpackTFWebSocket class.
        """
        self.ws_url = 'wss://ws.backpack.tf/events'
        self.headers = {'appid': 440, 'batch-test': True}
        self.save_user_data = SAVE_USER_DATA
        self.updated_items = []
        

        self.logger = SyncLogger("BackpackTFWebSocket")
        self.queue = ListingsQueueService()
        self.cache = CacheService()
        self.listings_db = ListingsDatabase()
        self.users_db = UsersDatabase()


    async def connect(self) -> None:
        """
        Connect to the Backpack.tf WebSocket.
        """
        while True:
            try:
                async for websocket in websockets.connect(
                    self.ws_url, 
                    extra_headers=self.headers, 
                    max_size=None,
                    ping_interval=60,
                    ping_timeout=120
                    ):
                    async for messages in websocket:
                        messages = orjson.loads(messages)
                        if isinstance(messages, list):
                            self.queue.add_updates(messages)
                            self.logger.write_log("info", f"Received {len(messages)} messages")
                            
                        sleep_time = math.ceil(self.queue.count_updates() / 2000)
                        if sleep_time > 0:
                            await asyncio.sleep(sleep_time)
            except websockets.exceptions.ConnectionClosedError:
                self.logger.write_log("error", "Connection closed")
                await asyncio.sleep(1)
                continue
            except Exception as e:
                self.logger.write_log("error", f"Failed to connect: {e}")
                await asyncio.sleep(60)
                continue


    async def handle_messages(self) -> None:
        """
        Handle messages from the Backpack.tf WebSocket.
        """
        while True:
            try:
                await asyncio.sleep(1)
                updates_in_queue = self.queue.count_updates()
                if updates_in_queue > 0:
                    batch = self.queue.get_updates()
                    if not batch:
                        continue

                    self.logger.write_log("info", f"Processing {len(batch)} messages, left {updates_in_queue} messages")
                    start_time = time.time()
                    for message in batch:
                        try:
                            payload = message['payload']

                            item = payload.get('item', {})
                            if not item or not isinstance(item, dict):
                                continue

                            item_name = item['name']
                            if not await self.cache.check_item_exists(item_name):
                                continue

                            item_sku = self.cache.get_sku_from_name(item_name)
                            if not item_sku:
                                item_sku = tf2.get_sku_from_name(item_name)

                            currencies = payload['currencies']
                            if "usd" in currencies:
                                continue

                            intent = payload['intent']
                            steamID = payload['steamid']
                            listing_id = payload['id'] if intent == "sell" else f"buy_440_{steamID}"

                            event = message['event']
                            if event == "delete":
                                await self.listings_db.delete(item_sku, listing_id)
                                self.logger.write_log("info", f"Deleted listing ({listing_id}) for {item_name}")
                                continue

                            data = {
                                "_id": listing_id,
                                "bumpAt": payload["bumpedAt"],
                                "buyoutOnly": payload.get("buyoutOnly", False),
                                "currencies": currencies,
                                "details": payload.get("details", ""),
                                "intent": intent,
                                "listedAt": payload["listedAt"],
                                "name": item_name,
                                "sku": item_sku,
                                "steamID": steamID,
                                "tradeOffersPreferred": payload.get("tradeOffersPreferred", False),
                            }

                            if payload.get("userAgent"):
                                data["userAgent"] = payload["userAgent"]

                            if item.get("spells"):
                                spells = []
                                for spell in item["spells"]:
                                    spell_name = spell["name"]
                                    defindex, id = get_spell_id(spell_name)
                                    spells.append({"defindex": defindex, "id": id, "name": spell_name})
                                data["spells"] = spells

                            if item.get("paint"):
                                data["paint"] = {"id": item["paint"]["id"], "name": item["paint"]["name"]}

                            if item.get("strangeParts"):
                                strange_parts = []
                                for part in item["strangeParts"]:
                                    strange_parts.append({"id": part["killEater"]["id"], "name": part["killEater"]["name"]})
                                data["strangeParts"] = strange_parts

                            if item.get("killstreaker"):
                                data["killstreaker"] = {"id": item["killstreaker"]["id"], "name": item["killstreaker"]["name"]}

                            if item.get("sheen"):
                                data["sheen"] = {"id": item["sheen"]["id"], "name": item["sheen"]["name"]}

                            await self.listings_db.update(item_sku, data)

                            if item_sku not in [i["sku"] for i in self.updated_items]:
                                self.updated_items.append({"sku": item_sku, "name": item_name})

                            self.logger.write_log("info", f"Updated listing ({listing_id}) for {item_name}")

                            if self.save_user_data and payload.get("user"):
                                payload["user"]["_id"] = payload["user"]["id"]
                                await self.users_db.insert(payload["user"])
                        except Exception as e:
                            self.logger.write_log("error", f"Failed to process message: {e}")

                    time_taken = time.time() - start_time
                    self.logger.write_log("info", f"Processed {len(batch)} messages in {time_taken:.2f}s (avg: {time_taken / len(batch):.4f}s/message)")
            except Exception as e:
                self.logger.write_log("error", f"Failed to handle messages: {e}")
                continue
