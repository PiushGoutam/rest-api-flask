from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import PlainStoreSchema, StoreSchema
from models import StoresModel
from db import db
from sqlalchemy.exc import IntegrityError, NoForeignKeysError
from flask_jwt_extended import jwt_required

blp = Blueprint("stores", __name__, description="Perform operations on stores")

@blp.route('/store')
class StoreList(MethodView):

    @jwt_required()
    @blp.response(200, PlainStoreSchema(many=True))
    def get(self):
        return StoresModel.query.all()

    @jwt_required()
    @blp.arguments(PlainStoreSchema)
    @blp.response(201, PlainStoreSchema)
    def post(self, store_data):
        store = StoresModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with same name already exists!")            
    
        return store

@blp.route('/store/<int:store_id>')  
class Store(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoresModel.query.get_or_404(store_id)
        return store
    
    @jwt_required()
    def delete(self, store_id):
        store = StoresModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted successfully!"}, 200


