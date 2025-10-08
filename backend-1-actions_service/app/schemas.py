from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    language: Optional[str] = "en"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    language: str
    class Config:
        orm_mode = True

class ActionCreate(BaseModel):
    user_id: int
    type: str
    payload: Optional[Dict[str, Any]] = None

class ActionOut(BaseModel):
    id: int
    user_id: int
    type: str
    payload: Optional[Dict[str, Any]]
    created_at: datetime
    class Config:
        orm_mode = True

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    body: str
    metadata: Optional[Dict[str, Any]] = None
    deliver_immediately: Optional[bool] = True

class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    metadata: Optional[Dict[str, Any]]
    delivered: bool
    read: bool
    created_at: datetime
    class Config:
        orm_mode = True
