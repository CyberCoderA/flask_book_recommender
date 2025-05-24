from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class UserModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)

    def user_exists(username: str) -> bool:
        return db.session.query(UserModel).filter_by(username=username).first() is not None
    
    def retrieve_password(username: str) -> str:
        return db.session.query(UserModel.password).filter_by(username=username).first()
