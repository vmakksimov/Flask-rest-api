from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db

blp = Blueprint("Items", __name__, description="Operations for items")


@blp.route("/items")
class ItemsList(MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request_data):
        item = ItemModel(**request_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Something went wrong!")

        return item


@blp.route("/items/<int:item_id>")
class Items(MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, request_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.type = request_data["type"]
            item.price = request_data["price"]
        else:
            item = ItemModel(id=item_id, **request_data)
        db.session.add(item)
        db.session.commit()
        return item

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges required.")

        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted!"}
