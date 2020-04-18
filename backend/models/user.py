from models import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id: int = db.Column(db.Integer, primary_key=True)
    first_name: str = db.Column(db.String(30), nullable=False)
    last_name: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(128), nullable=False)
    password: str = db.Column(db.String(256), nullable=True)
    active: bool = db.Column(db.Boolean, nullable=False, default=True)
    timestamp = db.Column(db.Date)

    @staticmethod
    def get_by_email(email):
        return db.session.query(UserModel).filter_by(email=email).first()

    @staticmethod
    def get_by_id(id_user: int):
        return UserModel.query.filter_by(id=id_user).first()

    @staticmethod
    def get_by_ids(ids_user):
        return UserModel.query.filter(UserModel.id.in_(ids_user)).all()

    @staticmethod
    def list_all():
        return UserModel.query.order_by(UserModel.first_name).all()

    @staticmethod
    def authenticate(email, password):
        user = UserModel.query.filter_by(email=email).first()
        if user and user.active:
            if password == user.password:
                return user
        return None

    def save(self):
        db.session.merge(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
