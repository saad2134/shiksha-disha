from typing import Dict
from fastapi import WebSocket
import asyncio

# Simple in-memory connection manager. For multi-instance use Redis Pub/Sub or Socket.IO.
class ConnectionManager:
    def __init__(self):
        self.active: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active:
            del self.active[user_id]

    async def send_personal(self, user_id: int, message: dict):
        ws = self.active.get(user_id)
        if ws:
            try:
                await ws.send_json(message)
            except Exception as e:
                # connection probably dead
                self.disconnect(user_id)

manager = ConnectionManager()
