from ws.backpack_tf import BackpackTFWebSocket
from utils.queue import ListingsQueueService
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager  
from utils.cache import CacheService
from utils.logger import SyncLogger
import asyncio


listings_queue = ListingsQueueService()
logger = SyncLogger("WsManagerAPI")
bptf_ws = BackpackTFWebSocket()
cache = CacheService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.

    Args:
        app (FastAPI): FastAPI application.
    """
    logger.write_log("info", "Starting API server lifespan")
    asyncio.gather(
        bptf_ws.connect(), 
        bptf_ws.handle_messages(),
        )
    yield
    logger.write_log("info", "Stopping API server lifespan")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: Health check response.
    """
    try:
        logger.write_log("info", "Health check successful")
        return {"status": "ok"}
    except Exception as e:
        logger.write_log("error", f"Failed to perform health check: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.post("/item")
async def add_item_to_cache(item: dict) -> dict:
    """
    Add an item to the cache.

    Args:
        item (dict): A dictionary containing item details, including SKU.

    Returns:
        dict: A response indicating the result of the operation.
    """
    try:
        item_sku = item.get("item_sku")
        if not item_sku:
            raise HTTPException(status_code=400, detail="SKU is required.")
        
        cache.add_item(item_sku)
        return {"success": True, "message": "Item added to cache successfully."}
    except Exception as e:
        logger.write_log("error", f"Failed to add item to cache: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.delete("/queue")
async def delete_item_updates(data: dict) -> dict:
    """
    Remove an item's updates from the listing updates queue.

    Args:
        data (dict): Input data containing the item's SKU.

    Returns:
        dict: A response indicating the result of the operation.
    """
    try:
        item_sku = data.get("item_sku")
        if not item_sku:
            raise HTTPException(status_code=400, detail="Item SKU is required.")
        
        listings_queue.remove_updates(item_sku)
        return {"success": True, "message": "Item updates successfully removed from the queue."}
    except Exception as e:
        logger.write_log("error", f"Error removing item updates from queue: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@app.get("/item-updates")
async def fetch_item_updates() -> list:
    """
    Retrieve the latest updates on item listings.

    Returns:
        list: A list of updated item details.
    """
    try:
        updates = bptf_ws.updated_items.copy()
        bptf_ws.updated_items.clear()
        return updates
    except Exception as e:
        logger.write_log("error", f"Failed to fetch item updates: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
