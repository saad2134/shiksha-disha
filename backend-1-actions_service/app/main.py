from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .db import Base, engine
from . import models
from .api import actions, notifications
from .realtime import manager

app = FastAPI(title="ShikshaDisha Backend - Actions & Notifications")

# Create tables (for demo). Use Alembic migrations for prod.
Base.metadata.create_all(bind=engine)

app.include_router(actions.router)
app.include_router(notifications.router)

@app.websocket("/ws/notifications/{user_id}")
async def notifications_ws(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # simple ping/pong or client messages; echo back
            await websocket.send_text(f"server received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
