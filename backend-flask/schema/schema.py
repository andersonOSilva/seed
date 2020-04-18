from models import db
from models.user import UserModel

from os import environ
# importar model aqui

from sqlalchemy import create_engine


class Schema:
    @staticmethod
    def migration():
        # aqui alteramos o banco
        engine = create_engine(environ.get('SQLALCHEMY_DATABASE_URI'))
        # <ClassModelName>.__table__.drop(engine)
        db.create_all()
