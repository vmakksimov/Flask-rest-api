import os
import redis
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_smorest import Api
from flask_migrate import Migrate
from resourses.store import blp as StoreBlueprint
from resourses.items import blp as ItemBlueprint
from resourses.tag import blp as TagBlueprint
from resourses.user import blp as UserBlueprint
from db import db
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from redis import Redis
from rq import Queue

load_dotenv()


def create_app():
    app = Flask(__name__)

    connection = redis.from_url(
        os.getenv('REDIS_URI')
    )
    app.queue = Queue("emails", connection=connection)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "STORES REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        os.getenv('POSTGRES_URI')
    )
    app.config["REDIS_URL"] = (
        os.getenv('REDIS_URL')
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # initialize the SQLAlchemy and connects it to the app
    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db, render_as_batch=True)

    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)
    redis_db = Redis(app, "REDIS")

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "Token is not fresh.", "error": "fresh_token_required."}
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_is_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Token has been revoked.", "error": "Token revoked."}),
            401,
        )

    @jwt.additional_claims_loader
    # Look into the dabase and check if user is admin
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Token has expired.", "error": "expired token."}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid token."}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "Authorization required.",
                }
            ),
            401,
        )

    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    return app


myapp = create_app()

if __name__ == "__main__":
    myapp.run()
