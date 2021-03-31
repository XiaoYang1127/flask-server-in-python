import hashlib
from passlib.apps import custom_app_context
from flask_login import AnonymousUserMixin, UserMixin

from .base import db, Column
from .mixins import CTimestampMixin, CQueryMixin


class CUser(CTimestampMixin, CQueryMixin, db.Model, UserMixin):
    __tablename__ = "tbl_user"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(25))
    email = Column(db.String(25))
    password_hash = Column(db.String(128), nullable=True)

    def __str__(self):
        return f"<{self.name}:{self.email} in {self.__tablename__}>"

    def serialize_list(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    def serialize_detail(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.serialize_time(self.created_at),
            "updated_at": self.serialize_time(self.updated_at)
        }

    def serialize_simple(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return self.password_hash and custom_app_context.verify(password, self.password_hash)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

    def get_id(self):
        identity = hashlib.md5("{},{}".format(
            self.email, self.password_hash).encode()).hexdigest()
        return "{0}-{1}".format(self.id, identity)


class CAnonymousUser(AnonymousUserMixin):
    pass
