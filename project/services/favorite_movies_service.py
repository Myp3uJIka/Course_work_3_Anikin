from project.dao import MovieDAO
from project.dao.favorite_movie import FavoriteMovieDAO
from project.schemas.favorite_movie import FavoriteMovieSchema
from project.services.base import BaseService


class FavoriteMovieService(BaseService):
    def get_by_user_id(self, user_id):
        movies = FavoriteMovieDAO(self._db_session).get_by_user_id(user_id)
        try:
            return FavoriteMovieSchema(many=True).dump(movies)
        except:
            return FavoriteMovieSchema().dump(movies)

    def create(self, m_id, user_id):
        movie = MovieDAO(self._db_session).get_by_id(m_id)
        data = {
            "user_id": user_id,
            "movie_id": movie.id
        }
        return FavoriteMovieDAO(self._db_session).create(data)

    def delete(self, fm_id, user_id):
        return FavoriteMovieDAO(self._db_session).delete(fm_id, user_id)
