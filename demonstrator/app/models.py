from sqlalchemy import JSON
from app import db
from flask_sqlalchemy import SQLAlchemy

class Things(db.Model):
    __tablename__ = "public.\"THINGS\""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(120), index=True, unique=True)
    properties = db.Column(JSON)

    def __repr__(self):
        return '<Properties %r>' % self.name