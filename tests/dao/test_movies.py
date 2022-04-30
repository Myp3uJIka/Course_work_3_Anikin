import pytest

from project.dao import MovieDAO
from project.dao.models import Movie


class TestMoviesDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = MovieDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        movie = Movie(
            title="Король Ричард",
            description="Комптон, 1988 год.",
            trailer="None",
            year="2021",
            rating="7.""5",
            genre_id="1",
            director_id="1"
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def movie_2(self, db):
        movie = Movie(
            title="Первый встречный",
            description="Поп-дива Кэт Вальдез и ее жених Бастиан — самая обсуждаемая пара года",
            trailer="None",
            year="2022",
            rating="6.1",
            genre_id="2",
            director_id="2"
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    def test_get_movie_by_id(self, movie_1):
        assert self.dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self):
        assert self.dao.get_by_id(1) is None

    def test_get_all_movies(self, movie_1, movie_2):
        assert self.dao.get_all() == [movie_1, movie_2]

    def test_get_filtered_movies(self, movie_1, movie_2):
        assert self.dao.get_filtered_movies(status="new") == [movie_2, movie_1]