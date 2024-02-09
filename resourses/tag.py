from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel, TagModel, ItemModel
from schemas import TagSchema, ItemSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations for stores")


@blp.route("/store/<int:store_id>/tag")
class TagStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, request_data, store_id):
        new_tag = TagModel(**request_data, store_id=store_id)
        try:
            db.session.add(new_tag)
            db.session.commit()
        except Exception as e:
            abort(500, message={e})
        return new_tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            abort(500, message={e})

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            abort(500, message={e})

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202, description="Delets a tag if no item has tag with it.")
    @blp.alt_response(404, description="Returned if the tag is find for more than one.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted!"}

        abort(
            400,
            message="Could not delete the tag. Make sure tag is not associated with any items and then try again",
        )
