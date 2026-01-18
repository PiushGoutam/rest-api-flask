from db import db

class StoresModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    items = db.relationship("ItemsModel",back_populates="store", cascade="all, delete, delete-orphan")
    tags = db.relationship("TagsModel", back_populates="store", cascade="all, delete, delete-orphan")
