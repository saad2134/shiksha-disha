from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .db import Base, engine
from . import models
from .api import users_router, actions_router, notifications_router, behavior_router, streak_router, auth_router
from .realtime import manager
from .config import settings
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="ShikshaDisha Core API",
    description="""
    ## 🎓 ShikshaDisha Core Backend
    
    This is the main backend service handling:
    - **User Management** - User accounts and profiles
    - **Action Tracking** - Track user activities and events
    - **Notifications** - Push notifications, email, and real-time alerts
    - **Learning Sessions** - Track engagement and behavior
    - **Streaks & Gamification** - Daily streaks and activity tracking
    - **Real-time Updates** - WebSocket connections for live notifications
    
    ### Database Models
    - Users & Authentication
    - Actions & Events
    - Notifications
    - Learning Sessions
    - Behavior Events
    - User Engagement Profiles
    - Streaks & Activities
    
    ### API Version: 1.0.0
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(actions_router, prefix="/actions", tags=["actions"])
app.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
app.include_router(behavior_router, prefix="/behavior", tags=["behavior"])
app.include_router(streak_router, prefix="/streak", tags=["streak"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/", tags=["Root"])
def root():
    return {
        "service": "ShikshaDisha Core API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected"
    }


@app.websocket("/ws/notifications/{user_id}")
async def notifications_ws(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"server received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)


@app.websocket("/ws/presence/{user_id}")
async def presence_ws(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        await manager.send_personal(user_id, {
            "type": "connected",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
