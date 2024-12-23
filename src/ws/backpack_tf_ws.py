from data.database import ListingsDatabase, UsersDatabase
from utils.config import SAVE_USER_DATA
from utils.logger import SyncLogger
from collections import deque
from utils.utils import *
import websockets
import asyncio
import json
import time
import math


class BackpackTFWebSocket:

    def __init__(self) -> None:
        """
        Initialize the BackpackTFWebSocket class.
        """
        self.ws_url = 'wss://ws.backpack.tf/events'
        self.headers = {'appid': 440, 'batch-test': True}
        
        self.queue = deque()
        self.updated_listings = []

        self.logger = SyncLogger("BackpackTFWebSocket")
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
                        messages = json.loads(messages)
                        if isinstance(messages, list):
                            self.queue.extend(messages)
                            self.logger.write_log("info", f"Received {len(messages)} messages")
                            
                        sleep_time = math.ceil(len(self.queue) / 2000)
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
                if self.queue:
                    batch = [self.queue.popleft() for _ in range(min(len(self.queue), 2000))]
                    if not batch:
                        continue

                    self.logger.write_log("info", f"Processing {len(batch)} messages, left {len(self.queue)} messages")
                    start_time = time.time()
                    for message in batch:
                        try:
                            await asyncio.sleep(0.002)
                            payload = message['payload']
                            item = payload['item']
                            item_name = item['name']
                            item_sku = tf2.getSkuFromName(item_name)

                            if not await self.listings_db.check_collection(item_sku):
                                continue

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
                            
                            if item_sku not in [listing["sku"] for listing in self.updated_listings]:
                                self.updated_listings.append({"sku": item_sku, "name": item_name})

                            if SAVE_USER_DATA and payload.get("user"):
                                payload["user"]["_id"] = payload["user"]["id"]
                                await self.users_db.insert(payload["user"])
                        except Exception as e:
                            self.logger.write_log("error", f"Failed to process message: {e}")

                    time_taken = time.time() - start_time
                    self.logger.write_log("info", f"Processed {len(batch)} messages in {time_taken:.2f}s (avg: {time_taken / len(batch):.4f}s/message)")
            except Exception as e:
                self.logger.write_log("error", f"Failed to handle messages: {e}")
                continue
