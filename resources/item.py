from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import PlainItemSchema, ItemSchema, ItemUpdateSchema
from models import ItemsModel
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("items", __name__, description="Perform operations on items")

@blp.route('/item')
class ItemList(MethodView):

    @jwt_required()
    @blp.response(200, PlainItemSchema(many=True))
    def get(self):
        return ItemsModel.query.all()

    @jwt_required()
    @blp.arguments(PlainItemSchema)
    @blp.response(201, PlainItemSchema)
    def post(self, item_data):

        if ItemsModel.query.filter(ItemsModel.store_id == item_data['store_id'], ItemsModel.name == item_data['name']).first():
             abort(400, message="A item with same name already exists in this store!")   

        item = ItemsModel(**item_data)
        db.session.add(item)
        db.session.commit()    
        return item

@blp.route('/item/<int:item_id>')
class Item(MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return ItemsModel.query.get_or_404(item_id)
    
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self,item_data, item_id):
        item = ItemsModel.query.get(item_id)
        if item:
            item.name = item_data['name']
            item.price = item_data['price']
        else:
            item = ItemsModel(**item_data, id=item_id)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))
        
        return item

    @jwt_required()    
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get('is_admin'):
            abort(400, message="Admin Credentials required!")
        item = ItemsModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))
        return {"message": "Item deleted successfully from the store"}
