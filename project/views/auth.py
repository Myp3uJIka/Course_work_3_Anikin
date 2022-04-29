from flask import request
from flask_restx import Namespace, Resource, abort

from project.services.users_service import UsersService
from project.setup_db import db
from project.tools.security import create_tokens, create_tokens_from_token, check_correct_fill

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class RegisterView(Resource):
    @auth_ns.response(200, "OK")
    def post(self):
        """Create user"""
        if not check_correct_fill(request.json):
            abort(400, message="Email, или пароль, не может содержать менее 8 символов")
        try:
            UsersService(db.session).create(request.json)
            return '', 201
        except Exception:
            abort(400, message="Данный логин уже используется")


@auth_ns.route("/login/")
class LoginView(Resource):
    def post(self):
        """Check user's email and password"""
        try:
            user = UsersService(db.session).get_by_email_password(request.json)
            tokens = create_tokens(user)
            return tokens, 200
        except Exception:
            abort(400, message="Логин, либо пароль, введён неверно")

    def put(self):
        """Get new tokens from token"""
        try:
            return create_tokens_from_token(request.json), 200
        except Exception:
            abort(400, message="Токен не является валидным")
