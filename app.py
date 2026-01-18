from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager, get_jwt
from flask_migrate import Migrate
import os
from db import db
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST



def create_app(db_url = None):

    app = Flask(__name__)

    app.config['API_TITLE'] = "Stores API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABSE_URI', "sqlite:///data.db")
    app.config['JWT_SECRET_KEY'] = "piush"

    
    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "This token has been revoked! Please login again!",
            "error": "token_invalid"
        }), 400


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "Invalid JWT token!. Please use a correct jwt token!",
            "error": "token_invalid"
        }), 400
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "Expired JWT token!. Please use a correct jwt token!",
            "error": "token_expired"
        }), 400
    
    @jwt.unauthorized_loader
    def unauthorized_token_callback(error):
        return jsonify({
            "message": "Unauthorized JWT token!. Please use a correct jwt token!",
            "error": "token_unauthorized"
        }), 400
    
    @jwt.additional_claims_loader
    def additional_claims_callback(identity):
        if identity == '1':
            return {"is_admin": True}
        return {"is_admin": False}




    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    db.init_app(app)
    
    with app.app_context() as context:
        db.create_all()
    migrate = Migrate(app, db)
    return app

