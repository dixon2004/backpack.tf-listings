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


    async def get_item_updates(self) -> list:
        """
        Get item updates from the websocket manager.
        
        Returns:
            list: List of item updates.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.url}/item-updates", timeout=10) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            self.logger.write_log("error", f"Failed to get item updates: {e}")
