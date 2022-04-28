from flask import request
from flask_restx import Namespace, Resource, abort

from project.services.users_service import UsersService
from project.setup_db import db
from project.tools.security import auth_required, generate_password_digest, get_user_from_token, \
    compare_password

users_ns = Namespace("user")


@users_ns.route('/')
class UsersView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    def get(self):
        """Get all users"""
        return UsersService(db.session).get_all(), 200

    def patch(self):
        """Update user's table"""
        try:
            req_json = request.json
            req_json['id'] = get_user_from_token(request.headers)['id']
            UsersService(db.session).update(req_json)
            return '', 204
        except Exception:
            abort(400, "Bad request")


@users_ns.route('/password/')
class SecurityView(Resource):
    @auth_required
    def put(self):
        """Change password"""
        try:
            req_json = request.json
            user_data = get_user_from_token(request.headers)
            req_json['current_password'] = UsersService(db.session).get_user_password(user_data['id'])
            if compare_password(req_json):
                data = {
                    "id": user_data['id'],
                    "password": generate_password_digest(req_json['new_password'])
                }
                UsersService(db.session).update(data)
                return '', 204
            else:
                abort(400, message="Old paasword is incorrect")
        except Exception:
            (400, "Bad request")
