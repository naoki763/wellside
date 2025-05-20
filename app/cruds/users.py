from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.model import User
from app.schemas.users import UserCreate


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except SQLAlchemyError as se:
        # ログ出力など適宜ハンドリングしてください
        print(f"[get_users] SQLAlchemyError: {se}")
        return []


def create_user(db: Session, request_body: UserCreate):
    try:
        new_user = User()
        new_user.user_id = request_body.user_id
        new_user.password = request_body.password
        new_user.username = request_body.username
        new_user.email = request_body.email
        new_user.created_at = datetime.now()
        new_user.updated_at = datetime.now()

        db.add(new_user)
        db.commit()
        print("保存しました")
    except SQLAlchemyError as se:
        # ログ出力など適宜ハンドリングしてください
        print(f"[get_users] SQLAlchemyError: {se}")
        return []
