from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from data.database import ListingsDatabase, UsersDatabase
from ws.backpack_tf_ws import BackpackTFWebSocket
from contextlib import asynccontextmanager  
from utils.token import AuthorizationToken
from api.backpack_tf import BackpackTFAPI
from utils.port import PortConfiguration
from utils.config import save_user_data
from utils.tasks import BackgroundTasks
from utils.utils import check_sku
from utils.log import write_log
import uvicorn
import asyncio
import json


bptf = BackpackTFAPI()
users_db = UsersDatabase()
bptf_ws = BackpackTFWebSocket()
listings_db = ListingsDatabase()
port_config = PortConfiguration()
auth_token = AuthorizationToken()
background_tasks = BackgroundTasks()


@asynccontextmanager
async def lifespan(app: FastAPI):
    write_log("info", "Starting API server lifespan")
    if not save_user_data:
        await users_db.drop_database()

    asyncio.gather(
        bptf_ws.connect(), 
        bptf_ws.handle_messages(),
        background_tasks.refresh_listings()
        )
    yield
    write_log("info", "Ending API server lifespan")


app = FastAPI(lifespan=lifespan)
        

@app.get("/listings")
async def get_listings(request: Request, sku: str):
    try:
        token = request.headers.get("Authorization", "")
        if not auth_token.token_valid(token):
            raise HTTPException(status_code=401, detail="Unauthorized.")

        if not check_sku(sku):
            raise HTTPException(status_code=400, detail="Invalid SKU.")
        
        if await listings_db.check_collection(sku):
            listings = await listings_db.get(sku)
        else:
            listings = await bptf.get_listings(sku)

        if not listings:
            raise HTTPException(status_code=404, detail="Listings not found.")
        
        return listings
    except Exception as e:
        write_log("error", f"Failed to get listings: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@app.delete("/listings/{sku}")
async def delete_listings(request: Request, sku: str):
    try:
        token = request.headers.get("Authorization", "")
        if not auth_token.token_valid(token):
            raise HTTPException(status_code=401, detail="Unauthorized.")

        if not check_sku(sku):
            raise HTTPException(status_code=400, detail="Invalid SKU.")
        
        await listings_db.delete_all(sku)
        return {"success": True}
    except Exception as e:
        write_log("error", f"Failed to delete listings: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@app.get("/user")
async def get_user(request: Request, steamid: str):
    try:
        token = request.headers.get("Authorization", "")
        if not auth_token.token_valid(token):
            raise HTTPException(status_code=401, detail="Unauthorized.")
        
        if not save_user_data:
            return {"success": False, "message": "User data saving is disabled."}

        user = await users_db.get(steamid)
        return user
    except Exception as e:
        write_log("error", f"Failed to get user: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

class ConnectionManager:

    def __init__(self) -> None:
        """
        Initialize the connection manager.
        """
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
        except Exception as e:
            write_log("error", f"[ConnectionManager] Failed to connect: {e}")


    def disconnect(self, websocket: WebSocket) -> None:
        """
        Disconnect from the WebSocket.
        
        Args:
            websocket (WebSocket): WebSocket connection.
        """
        try:
            self.active_connections.remove(websocket)
        except Exception as e:
            write_log("error", f"[ConnectionManager] Failed to disconnect: {e}")


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
                    write_log("error", f"[ConnectionManager] Failed to broadcast message: {e}")
        except Exception as e:
            write_log("error", f"[ConnectionManager] Failed to broadcast: {e}")


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1)
            if not bptf_ws.updated_listings:
                continue

            await manager.broadcast(bptf_ws.updated_listings)
            bptf_ws.updated_listings.clear()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    

if __name__ == "__main__":
    port = port_config.get_port()
    if not port:
        write_log("error", "No available port found.")
        exit(1)

    write_log("info", f"Starting the API server on port {port}.")
    uvicorn.run(app, host="127.0.0.1", port=port)
