from flask import request, jsonify
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource
from models.user import UserModel
from datetime import date, datetime


class UserResource(Resource):

    def _list_user(self):
        users = UserModel.list_all()

        return list(map(lambda user: {
            'id': user.id,
            'name': user.first_name,
            'email': user.email,
            'active': user.active,
            'password': user.password
        }, users))

    # @jwt_required
    def get(self):
        try:
            return self._list_user()
        except Exception as e:
            return f"{e}", 500

    def post(self):
        item = request.get_json() if request.get_json() else request.form

        try:
            if item:
                model = UserModel()
                model.first_name = item['first_name']
                model.last_name = item['last_name']
                model.email = item['email']
                model.active = item['active'] if 'active' in item else True
                model.password = item['password']
                model.timestamp = date.today()
                model.save()

                return 'created', 201
            else:
                return 'not created, invalid payload', 400
        except Exception as e:
            return f"{e}", 500



class UserDetailResource(Resource):

    def _get_user(self, id_user):
        user = UserModel.get_by_id(id_user)

        if user is None:
            return {'message': 'User not found'}, 404

        return {
            'id': user.id,
            'name': user.first_name,
            'email': user.email,
            'active': user.active
        }

    @jwt_required
    def get(self, id):
        try:
            id_user = id
            return self._get_user(id_user)

        except Exception as e:
            return f"{e}", 500

    # @jwt_required
    def put(self, id):
        item = request.get_json() if request.get_json() else request.form

        try:
            if item:
                model = UserModel.get_by_id(id)
                if 'first_name' in item:
                    model.first_name = item['first_name']
                if 'last_name' in item:
                    model.last_name = item['last_name']
                if 'email' in item:
                    model.email = item['email']
                if 'active' in item:
                    model.active = item['active'] if 'active' in item else True
                if 'password' in item:
                    model.password = item['password']
                model.save()

                return 'edited', 204
            else:
                return 'unedited, invalid payload', 400

        except Exception as e:
            return f"{e}", 500

    def delete(self, id):
        try:
            user = UserModel.get_by_id(id)
            user.delete()
            return 'No Content', 204

        except Exception as e:
            return f"{e}", 500
