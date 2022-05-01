from unittest.mock import MagicMock

import pytest

from project.dao import MovieDAO
from project.dao.models import Movie
from project.schemas import MovieSchema
from project.services import MoviesService


class TestMoviesService:
    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = MoviesService(db.session)

    @pytest.fixture
    def movie(self):
        return Movie(
            title="Плезантвиль",
            description="Дэвид Вагнер - дитя девяностых.",
            trailer="...",
            year="1998",
            rating="7.8",
            genre_id="1",
            director_id="1"
        )

    @pytest.fixture
    def movie_dao_mock(self, movie):
        MovieDAO.get_by_id = MagicMock(return_value=MovieSchema().dump(movie))
        MovieDAO.get_all = MagicMock(return_value=MovieSchema(many=True).dump([movie]))
        MovieDAO.get_filtered_movies = MagicMock(return_value=MovieSchema(many=True).dump([movie]))
        return MovieDAO

    def test_get_movie_by_id(self, movie_dao_mock, movie):
        assert self.service.get_item_by_id(movie.id) == MovieSchema().dump(movie)

    def test_get_all_movies(self, movie_dao_mock, movie):
        assert self.service.get_all_movies() == MovieSchema(many=True).dump([movie])

    def test_get_filtered_movies(self, movie_dao_mock, movie):
        assert self.service.get_filtered_movies({"page": 0}) == MovieSchema(many=True).dump([movie])
