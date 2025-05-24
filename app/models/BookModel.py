from app import db
from sqlalchemy import Integer, String
from datetime import datetime

class Books(db.model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.DateTime, default=datetime.utcnow)
    cover = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name