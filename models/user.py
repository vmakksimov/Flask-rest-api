from db import db
from sqlalchemy import UniqueConstraint


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String, nullable=False)
    # UniqueConstraint(email)
