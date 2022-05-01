from flask import request
from flask_restx import Resource, Namespace, abort

from project.exceptions import ItemNotFound
from project.services import MoviesService
from project.setup_db import db

movies_ns = Namespace("movies")


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.response(200, "OK")
    def get(self):
        """Get all movies"""
        filter_param = request.args
        if filter_param:
            return MoviesService(db.session).get_filtered_movies(filter_param), 200
        return MoviesService(db.session).get_all_movies(), 200


@movies_ns.route("/<int:movie_id>/")
class MovieView(Resource):
    # @movies_ns.response(200, "OK")
    # @movies_ns.response(404, "Movie not found")
    def get(self, movie_id: int):
        """Get movie by id"""
        try:
            return MoviesService(db.session).get_item_by_id(movie_id), 200
        except ItemNotFound:
            abort(404, message="Movie not found")
