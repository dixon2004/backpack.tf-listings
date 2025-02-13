from tasks.listings_updater import ListingsUpdater
from api.ws_manager import WebsocketManager
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from api.backpack_tf import BackpackTFAPI
from utils.logger import SyncLogger
import asyncio


logger = SyncLogger("ListingsManagerAPI")
listings_updater = ListingsUpdater()
ws_manager = WebsocketManager()
bptf = BackpackTFAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.

    Args:
        app (FastAPI): FastAPI application.
    """
    logger.write_log("info", "Starting API server lifespan")
    asyncio.create_task(listings_updater.run())
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
        

@app.get("/listings")
async def get_listings(item_sku: str) -> list:
    """
    Get Backpack.tf listings for a specific item.

    Args:
        item_sku (str): SKU of the item.
    
    Returns:
        list: List of listings.
    """
    try:
        listings = await bptf.get_listings(item_sku)

        if not listings:
            raise HTTPException(status_code=404, detail="Listings not found.")
        
        await ws_manager.add_item_to_cache(item_sku)

        return listings
    except Exception as e:
        logger.write_log("error", f"Failed to get listings: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
