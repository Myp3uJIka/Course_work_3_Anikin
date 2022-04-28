from marshmallow import Schema, fields


class FavoriteMovieSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    movie_id = fields.Int(required=True)
