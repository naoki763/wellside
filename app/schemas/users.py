from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    full_name: str


class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str


class UserCreateResponse(BaseModel):
    username: str
    full_name: str


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class Users(UserBase):
    users: list[User]
