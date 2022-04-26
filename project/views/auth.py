from flask import request
from flask_restx import Namespace, Resource

from project.services.users_service import UsersService
from project.setup_db import db
from project.tools.security import create_tokens, create_tokens_from_rtoken

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class RegisterView(Resource):
    def post(self):
        try:
            UsersService(db.session).create(request.json)
            return '', 201
        except Exception:
            return {"error": 'Данный логин уже используется.'}, 400


@auth_ns.route("/login/")
class LoginView(Resource):
    def post(self):
        try:
            user = UsersService(db.session).get_by_email_password(request.json)
            tokens = create_tokens(user)
            return tokens, 200
        except Exception as e:
            return {"error": 'Логин, либо пароль, введён неверно.'}, 400

    def put(self):
        return create_tokens_from_rtoken(request.json)
