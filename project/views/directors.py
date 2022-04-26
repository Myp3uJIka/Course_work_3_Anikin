from flask_restx import Resource, Namespace, abort

from project.exceptions import ItemNotFound
from project.services import DirectorsService
from project.setup_db import db

directors_ns = Namespace("directors")


@directors_ns.route("/")
class DirectorsView(Resource):
    @directors_ns.response(200, "OK")
    def get(self):
        """Get all directors"""
        return DirectorsService(db.session).get_all_directors()


@directors_ns.route("/<int:did>/")
class DirectorView(Resource):
    @directors_ns.response(200, "OK")
    @directors_ns.response(404, "Director not found")
    def get(self, did):
        """Get director by id"""
        try:
            return DirectorsService(db.session).get_item_by_id(did)
        except ItemNotFound:
            abort(404, message="Director not found")
