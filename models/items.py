from db import db 

class ItemsModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.String)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoresModel", back_populates="items",)
    tags = db.relationship("TagsModel", back_populates="items", secondary="tags_items",  lazy="dynamic")
    address = db.Column(db.String(200))