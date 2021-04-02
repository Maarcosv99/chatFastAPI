from fastapi import FastAPI, APIRouter, Request
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

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
            receive = await websocket.json_receive
            receive_text = await websocket.text_receive
            # Msg enviada
            if receive_text != 'echo':
                await manager.broadcast(receive)
        except WebSocketDisconnect:
            manager.disconnect(websocket)