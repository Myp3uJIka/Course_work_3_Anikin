from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genres.id"))
    genres = db.relationship('Genre')
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<User '{self.email}'>"
