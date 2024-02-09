from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from tasks import send_simple_message
from tasks import send_user_registration_email
from flask import current_app

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=sha256_crypt.encrypt(user_data["password"]),
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(
                500,
                message="The username may exists or the password is not sufficient.",
            )

        current_app.queue.enqueue(
            send_user_registration_email, user.email, user.username
        )
        # send_user_registration_email()
        send_simple_message(
            to=user.email,
            subject="Successfully Signed up!",
            body=f"Hello, {user.username} has succesfully signed up!",
        )

        return {"message": "User created successfully!"}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and sha256_crypt.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, "No such user.")


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(201, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User was deleted."}, 200


@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"non_refresh_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}
