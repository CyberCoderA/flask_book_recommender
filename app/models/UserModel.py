from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import json

class UserModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    prefferred_genres: Mapped[str] = mapped_column(String(255), nullable=True)

    def user_exists(username: str) -> bool:
        return db.session.query(UserModel).filter_by(username=username).first() is not None
    
    def retrieve_preffered_genres(username: str) -> str:
        return db.session.query(UserModel.prefferred_genres).filter_by(username=username).first()
    
    def retrieve_password(username: str) -> str:
        return db.session.query(UserModel.password).filter_by(username=username).first()
    
    def retrieve_user_id(username: str) -> int:
        return db.session.query(UserModel.id).filter_by(username=username).first()
    
    def retrieve_username(id: str) -> str:
        return db.session.query(UserModel.username).filter_by(id=id).first()
    
    def retrieve_user(username: str) -> str:
        return db.session.query(UserModel).filter_by(username=username).first()
    
    def delete_user(id: str) -> str:
        user = db.session.query(UserModel).filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return "User deleted successfully."
        else:
            return "Delete failed, user not found."
    
    def update_user(username, new_password, new_username, id):
        user = db.session.query(UserModel).filter_by(username=username).first()

        if(user):
            user.password = new_password
            if(UserModel.retrieve_username(id) == new_username):
                return "Username already exists."
            else:
                user.username = new_username
                db.session.commit()
                return "Update successful!"
        else:
            return "Update failed!"
    
    def account_list():
        return db.session.query(UserModel).all()