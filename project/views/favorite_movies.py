from flask import request
from flask_restx import Namespace, Resource, abort

from project.exceptions import ItemNotFound
from project.services.favorite_movies_service import FavoriteMovieService
from project.setup_db import db
from project.tools.security import auth_required, get_user_from_token

favorite_movies_ns = Namespace("favorites/movies")

"""задача не решена, т.к. не был найден способ извлечения id пользователя"""


@favorite_movies_ns.route("/")
class FavoritesView(Resource):
    # @auth_required
    def get(self):
        user_id = 1
        # user_id = get_user_from_token(request.header)['id']
        try:
            return FavoriteMovieService(db.session).get_by_user_id(user_id), 200
        except ItemNotFound:
            abort(404, message="Favorite movie not found")


@favorite_movies_ns.route("/<int:m_id>/")
class FavoriteView(Resource):
    # @auth_required
    def get(self):
        user_id = 1
        # user_id = get_user_from_token(request.header)['id']
        try:
            return FavoriteMovieService(db.session).get_by_user_id(user_id), 200
        except ItemNotFound:
            abort(404, message="Favorites movies not found")

    def post(self, m_id: int):
        user_id = 1
        # user_id = get_user_from_token(request.header)['id']
        try:
            return FavoriteMovieService(db.session).create(m_id, user_id)
        except Exception:
            abort(404, message="The movie cannot be added to favorites")

    def delete(self, m_id: int):
        user_id = 1
        # user_id = get_user_from_token(request.header)['id']
        try:
            return FavoriteMovieService(db.session).delete(m_id, user_id)
        except Exception:
            abort(404, message="The movie cannot be deleted")
