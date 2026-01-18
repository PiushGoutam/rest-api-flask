from flask_smorest import abort, Blueprint
from flask.views import MethodView
from models import TagsModel, StoresModel, ItemsModel, ItemsTagsModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import PlainTagSchema, TagSchema
from flask_jwt_extended import jwt_required

blp = Blueprint("tags", __name__, description="Perform operations on tags")

@blp.route('/store/<int:store_id>/tag')
class TagsInStore(MethodView):

    @jwt_required()
    @blp.arguments(PlainTagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        store = StoresModel.query.get_or_404(store_id)
        if TagsModel.query.filter(TagsModel.store_id == store_id, TagsModel.name == tag_data['name']).first():
            abort(400, message="A tag of same name already exists in thisa store!")
        tag = TagsModel(**tag_data)

        store.tags.append(tag)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))
        
        return tag

    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoresModel.query.get_or_404(store_id)
        return store.tags
    
@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagToItem(MethodView):
    @jwt_required()
    def post(self, item_id, tag_id):
        item = ItemsModel.query.get_or_404(item_id)
        tag = TagsModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(400, message="The item and the tag belong to different store! Cant be linked!")
        
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))
        return {"message": "Item and tag successfully linked!"}, 201
    
    @jwt_required()
    def delete(self, item_id, tag_id):
        item = ItemsModel.query.get_or_404(item_id)
        tag = TagsModel.query.get_or_404(tag_id)    
        
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))
        return {"message": "Item and tag successfully unlinked!"}, 201

@blp.route('/tag/<int:tag_id>')
class Tag(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        return tag
    @jwt_required()  
    def delete(self, tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        if tag.items:
            abort(400, message="This tag has items linked to it!. Cannot delete!")
        else:
            db.session.delete(tag)
            db.session.commit()

        return {"message": "The tag has been deleted sucessfully"}, 200
