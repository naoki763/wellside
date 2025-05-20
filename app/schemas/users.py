from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    full_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str


class Users(BaseModel):
    users: list[UserBase]
