from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect as WSD
from typing import List
# Imports
from chat.router import router as chat_router

app = FastAPI(title='Chat Real-time')

app.mount('/assets', StaticFiles(directory='assets'), name='assets')
templates = Jinja2Templates(directory='templates')

# Import urls
app.include_router(chat_router)

#Socket chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

manager = ConnectionManager()

@app.websocket_route('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        try:
            # Msg recebida
            receive = await websocket.receive_json()
            # Msg enviada
            if 'message' in receive:
                await manager.broadcast(receive)
        except WebSocketDisconnect:
            manager.disconnect(websocket)