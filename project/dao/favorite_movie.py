from sqlalchemy.orm import scoped_session

from project.dao.models import FavoriteMovie


class FavoriteMovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one(self, movie_id, user_id):
        return self._db_session.query(FavoriteMovie).filter(FavoriteMovie.movie_id == movie_id,
                                                            FavoriteMovie.user_id == user_id).one_or_none()

    def get_by_user_id(self, user_id):
        return self._db_session.query(FavoriteMovie).filter(FavoriteMovie.id == user_id).all()

    def create(self, data):
        favorite_movie = FavoriteMovie(**data)
        self._db_session.add(favorite_movie)
        self._db_session.commit()

    def delete(self, fm_id, user_id):
        favorite_movie = self.get_one(fm_id, user_id)
        self._db_session.delete(favorite_movie)
        self._db_session.commit()
