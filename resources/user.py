from flask_smorest import abort, Blueprint
from flask.views import MethodView
from models import UsersModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import UserSchema
blp = Blueprint("users", __name__, description="Perform operations on users")
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from blocklist import BLOCKLIST

@blp.route('/register')
class Register(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UsersModel(username=user_data['username'],
                          password = pbkdf2_sha256.hash(user_data['password']))
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Username already taken!")
        except SQLAlchemyError as e:
            abort(400, message=str(e))
        
        return user

@blp.route('/login')
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):

        user = UsersModel.query.filter(UsersModel.username == user_data['username']).first_or_404()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200
        abort(400, message="Invalid credentials!")


@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UsersModel.query.get_or_404(user_id)
        return user
    

    def delete(self,user_id):
        user = UsersModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))
        return {"message": "User deleted successfully!"}


@blp.route('/logout')
class Logout(MethodView):

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        BLOCKLIST.add(jwt.get('jti'))

        return {"message": "User logged out successfully!"}


        
        
