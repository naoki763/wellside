from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.users import create_user, get_users
from app.database import get_db
from app.schemas.users import UserBase, UserCreate, Users

user_router = APIRouter()


@user_router.get("/users", tags=["users"], response_model=Users)
async def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> Users:
    users = get_users(db, skip=skip, limit=limit)
    response_data = [UserBase.model_validate(user) for user in users]
    return Users(users=response_data)


@user_router.post(
    "/users",
    tags=["users"],
    # response_model=UserCreate
)
async def register_user_for_login(
    request_body: UserCreate, db: Session = Depends(get_db)
):
    user = create_user(db=db, request_body=request_body)
    return user
