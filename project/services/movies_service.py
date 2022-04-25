from flask import current_app

from project.dao import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas import MovieSchema
from project.services.base import BaseService


class MoviesService(BaseService):
    def get_item_by_id(self, pk):
        movie = MovieDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self):
        movies = MovieDAO(self._db_session).get_all()
        return MovieSchema(many=True).dump(movies)

    def get_filtered_movies(self, filter_param):
        limit = 0
        offset = 0
        if filter_param.get("page"):
            limit = current_app.config["ITEMS_PER_PAGE"]
            offset = (filter_param.get("page") - 1) * limit
        status = filter_param.get("status")
        movies = MovieDAO(self._db_session).get_filtered_movies(limit=limit, offset=offset, status=status)
        return MovieSchema(many=True).dump(movies)

