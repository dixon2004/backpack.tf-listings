from database.listings import ListingsDatabase
from utils.logger import SyncLogger
from utils.config import BPTF_TOKEN
from utils.utils import *
import aiohttp
import asyncio
import random
import time


class BackpackTFAPI:

    def __init__(self) -> None:
        """
        Initialize the BackpackTFAPI class.
        """
        self.url = "https://backpack.tf/api"
        self.tokens = BPTF_TOKEN
        self.rate_limit = {}

        self.logger = SyncLogger("BackpackTFAPI")
        self.db = ListingsDatabase()


    async def call(self, url: str, params: dict) -> dict:
        """
        Call the Backpack.tf API.
        
        Args:
            url (str): API endpoint.
            params (dict): API parameters.
            
        Returns:
            dict: API response.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 429:
                    self.rate_limit[params["token"]] = time.time() + 30
                    raise Exception("Rate limit exceeded")
            
                response.raise_for_status()
                return await response.json()


    async def get_available_tokens(self) -> list:
        """
        Get available tokens, waiting for rate-limited tokens if necessary.
        
        Returns:
            list: List of available tokens.
        """
        max_attempts = 3
        loop = 0

        while loop < max_attempts:
            current_time = time.time()
            
            # Remove expired rate-limited tokens
            self.rate_limit = {token: expiry for token, expiry in self.rate_limit.items() if expiry > current_time}

            # Get available tokens
            available_tokens = [token for token in self.tokens if token not in self.rate_limit]
            if available_tokens:
                return available_tokens

            # Wait for rate-limited tokens
            if self.rate_limit:
                shortest_cooldown = (min(self.rate_limit.values()) - current_time) + 1
                await asyncio.sleep(shortest_cooldown)
            else:
                raise Exception("No tokens are available and no tokens are rate-limited")

            loop += 1

        raise Exception("Rate limit exceeded after maximum attempts")


    async def fetch_snapshots(self, name: str) -> list:
        """
        Fetch snapshots from the Backpack.tf API.
        
        Args:
            name (str): Name of the item.
            
        Returns:
            list: List of snapshots.
        """
        try:
            available_tokens = await self.get_available_tokens()
            params = {
                "sku": name,
                "appid": "440",
                "token": random.choice(available_tokens)
            }
            response = await self.call(f"{self.url}/classifieds/listings/snapshot", params)
            return response
        except Exception as e:
            self.logger.write_log("error", f"Failed to fetch snapshots: {e}")


    async def format_listing(self, listing: dict) -> dict:
        """
        Format the listing.
        
        Args:
            listing (dict): Listing data.
            
        Returns:
            dict: Formatted listing.
        """
        try:
            currencies = listing["currencies"]

            # Skip Marketplace.tf listings
            if "usd" in currencies:
                return

            intent = listing["intent"]
            steamID = listing["steamid"]
            listing_id = listing["item"]["id"] if intent == "sell" else f"buy_440_{steamID}"

            data = {
                "_id": listing_id,
                "bumpAt": listing["bump"],
                "buyoutOnly": bool(listing.get("buyout", False)),
                "currencies": currencies,
                "details": listing["details"],
                "intent": intent,
                "listedAt": listing["timestamp"],
                "steamID": steamID,
                "tradeOffersPreferred": bool(listing.get("offers", False)),
            }

            if listing.get("userAgent"):
                data["userAgent"] = listing["userAgent"]

            if listing["item"].get("attributes"):
                attributes = listing["item"]["attributes"]
                for attr in attributes:
                    defindex = int(attr.get("defindex"))
                    float_value = attr.get("float_value", None)

                    if float_value:
                        try:
                            float_value = int(float_value)
                        except ValueError:
                            float_value = float(float_value) if float_value else None
                    else:
                        float_value = None

                    if 1004 <= defindex <= 1009:
                        # Spells
                        if not data.get("spells"): data["spells"] = []
                        if not float_value: float_value = 1
                        data["spells"].append({"defindex": defindex, "id": float_value, "name": spells_attributes[defindex][float_value]})
                    elif defindex == 142:
                        # Paint
                        data["paint"] = {"id": float_value, "name": paints_attributes[float_value]}
                    elif defindex in [380, 382, 384]:
                        # Strange Parts
                        if not data.get("strangeParts"): data["strangeParts"] = []
                        data["strangeParts"].append({"id": float_value, "name": strange_parts_attributes[float_value]})
                    elif defindex == 2013:
                        # Killstreak effect
                        data["killstreaker"] = {"id": float_value, "name": killstreak_effects_attributes[float_value]}
                    elif defindex == 2014:
                        # Killstreak sheen
                        data["sheen"] = {"id": float_value, "name": killstreak_sheens_attributes[float_value]}

            return data
        except Exception as e:
            self.logger.write_log("error", f"Failed to format listing ({listing}): {e}")


    async def get_listings(self, sku: str) -> list:
        """
        Get listings from the Backpack.tf API.
        
        Args:
            sku (str): SKU of the item.
            
        Returns:
            list: List of formatted listings."""
        try:
            if "None" in sku:
                raise Exception("Invalid item SKU.")

            item_name = tf2.get_name_from_sku(sku)
            if not item_name:
                raise Exception("Invalid item name.")

            snapshots = await self.fetch_snapshots(item_name)
            if not isinstance(snapshots, dict):
                raise Exception("Invalid snapshots response from API.")
            
            listings = snapshots.get("listings")
            if not listings:
                raise Exception("No listings found.")
            
            formatted_listings = []
            listing_ids = []
            for listing in listings:
                formatted_listing = await self.format_listing(listing)
                if formatted_listing:
                    formatted_listing["sku"] = sku
                    formatted_listing["name"] = item_name

                    if formatted_listing["_id"] not in listing_ids:
                        formatted_listings.append(formatted_listing)
                        listing_ids.append(formatted_listing["_id"])

            await self.db.delete_all(sku)
            await self.db.insert(sku, formatted_listings)

            return formatted_listings
        except Exception as e:
            self.logger.write_log("error", f"Failed to get listings: {e}")
