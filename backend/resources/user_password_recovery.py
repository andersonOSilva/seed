from flask import request
from flask_restful import Resource
from models.user import UserModel
from re import match
from services.email import EmailService

PASSWORD_PATTERN = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})"


class UserPasswordRecoveryResource(Resource):
    def get(self):
        email = request.args['email']
        user = UserModel.get_by_email(email)

        if user:
            message = "email com link de recuperação"

            email_service = EmailService()
            email_service.send(to_address=user.email, message_content=message,
                               subject='VISTOCAR - Recuperação de senha')

            return {'message': 'Recovery message sent'}

        else:
            return {'message': 'User not found'}, 404

    def post(self):
        email = request.json.get('email')
        token = request.json.get('token')
        error = None

        user = UserModel.get_by_email(email)

        # Validations
        if not user:
            error = 'Usuário inválido'

        elif not match(PASSWORD_PATTERN, new_password):
            error = 'A senha não atende os critérios mínimos de complexidade'

        if error:
            return {'message': error}, 400

        user.password = UserModel.generate_hash(new_password)
        user.save()

        return None, 204
