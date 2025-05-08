from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from api.listings_manager import ListingsManager
from database.listings import ListingsDatabase
from api.ws_manager import WebsocketManager
from contextlib import asynccontextmanager  
from utils.token import AuthorizationToken
from database.users import UsersDatabase
from utils.config import SAVE_USER_DATA
from utils.cache import CacheService
from utils.logger import SyncLogger
from utils.utils import tf2
import asyncio
import json


logger = SyncLogger("ListingsServiceAPI")
listings_manager = ListingsManager()
auth_token = AuthorizationToken()
listings_db = ListingsDatabase()
ws_manager = WebsocketManager()
users_db = UsersDatabase()
cache = CacheService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.

    Args:
        app (FastAPI): FastAPI application.
    """
    logger.write_log("info", "Starting API server lifespan")
    if not SAVE_USER_DATA:
        await users_db.drop_database()
        logger.write_log("info", "Saving user data is disabled, dropped the users database")

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
async def get_listings(request: Request, sku: str) -> list:
    """
    Get listings for a specific item.
    
    Args:
        request (Request): Request object.
        sku (str): SKU of the item.
        
    Returns:
        list: List of listings.
    """
    try:
        token = request.headers.get("Authorization", "")
        if not auth_token.token_valid(token):
            raise HTTPException(status_code=401, detail="Unauthorized.")

        if not tf2.test_sku(sku):
            raise HTTPException(status_code=400, detail="Invalid SKU.")
        
        if await cache.check_item_exists(sku):
            listings = await listings_db.get(sku)
        else:
            cache.add_item(sku)
            listings = await listings_manager.get_listings(sku)

        if not listings:
            raise HTTPException(status_code=404, detail="Listings not found.")

        return listings
    except Exception as e:
        logger.write_log("error", f"Failed to get listings: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@app.delete("/listings/{sku}")
async def delete_listings(request: Request, sku: str) -> dict:
    """
    Delete listings for a specific item.
    
    Args:
        request (Request): Request object.
        sku (str): SKU of the item.
    
    Returns:
        dict: Response message.
    """
    try:
        token = request.headers.get("Authorization", "")
        if not auth_token.token_valid(token):
            raise HTTPException(status_code=401, detail="Unauthorized.")

        if not tf2.test_sku(sku):
            raise HTTPException(status_code=400, detail="Invalid SKU.")
        
        cache.remove_item(sku)
        await listings_db.delete_all(sku)
        return {"success": True}
    except Exception as e:
        logger.write_log("error", f"Failed to delete listings: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@app.get("/user")
async def get_user(request: Request, steamid: str) -> dict:
    """
    Get user data.
    
    Args:
        request (Request): Request object.
        steamid (str): SteamID of the user.
    
    Returns:
        dict: User data.
    """
    try:
        token = request.headers.get("Authorization", "")
        if not auth_token.token_valid(token):
            raise HTTPException(status_code=401, detail="Unauthorized.")
        
        if not SAVE_USER_DATA:
            return {"success": False, "message": "User data saving is disabled."}

        user = await users_db.get(steamid)
        return user
    except Exception as e:
        logger.write_log("error", f"Failed to get user: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

class ConnectionManager:

    def __init__(self) -> None:
        """
        Initialize the connection manager.
        """
        self.logger = SyncLogger("ConnectionManager")
        self.active_connections: list[WebSocket] = []


    async def connect(self, websocket: WebSocket) -> None:
        """
        Connect to the WebSocket.
        
        Args:
            websocket (WebSocket): WebSocket connection.
        """
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            self.logger.write_log("info", f"{websocket.client.host} connected")
        except Exception as e:
            self.logger.write_log("error", f"Failed to connect: {e}")


    def disconnect(self, websocket: WebSocket) -> None:
        """
        Disconnect from the WebSocket.
        
        Args:
            websocket (WebSocket): WebSocket connection.
        """
        try:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
            self.logger.write_log("info", f"{websocket.client.host} disconnected")
        except Exception as e:
            self.logger.write_log("error", f"Failed to disconnect: {e}")


    async def broadcast(self, message: dict) -> None:
        """
        Broadcast a message to all active connections.
        
        Args:
            message (dict): Message to broadcast.
        """
        try:
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    self.logger.write_log("error", f"Failed to broadcast: {e or 'Unknown error'}")
                    self.disconnect(connection)
        except Exception as e:
            self.logger.write_log("error", f"Failed to broadcast: {e}")


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint.
    
    Args:
        websocket (WebSocket): WebSocket connection.
    """
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1)
            item_updates = await ws_manager.get_item_updates()
            if not item_updates:
                continue

            await manager.broadcast(item_updates)
            logger.write_log("info", f"Item updates broadcasted: {len(item_updates)} items")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
