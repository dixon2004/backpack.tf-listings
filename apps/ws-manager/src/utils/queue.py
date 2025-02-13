from database.listings import ListingsDatabase
from utils.logger import SyncLogger
from collections import deque
from utils.utils import tf2


updates_queue = deque()


class ListingsQueueService:

    def __init__(self) -> None:
        """
        Initialize the ListingsQueueService class.
        """
        self.logger = SyncLogger("ListingsQueueService")
        self.db = ListingsDatabase()


    def count_updates(self) -> int:
        """
        Count the number of updates in the listing updates queue.

        Returns:
            int: Number of updates.
        """
        return len(updates_queue)


    def get_updates(self) -> list:
        """
        Get updates from the listing updates queue.

        Returns:
            list: List of items.
        """
        return [updates_queue.popleft() for _ in range(min(len(updates_queue), 2000))]


    def add_updates(self, items: list) -> None:
        """
        ADd updates to the listing updates queue.

        Args:
            items (list): List of items.
        """
        global updates_queue
        updates_queue.extend(items)


    def remove_updates(self, item_sku: str) -> None:
        """
        Remove updates from the listing updates queue.

        Args:
            item_sku (str): SKU of the item.
        """
        global updates_queue
        item_name = tf2.get_name_from_sku(item_sku)
        updates_queue = deque([item for item in updates_queue if item.get("payload").get("name") != item_name])
        self.logger.write_log("info", f"Removed updates from queue: {item_name}")
