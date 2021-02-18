import datetime
import hashlib
from sqlalchemy import exc

import config
import errors
from app import db


class BaseModelMixin:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck

    def upd(self):
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    advertisement = db.relationship('Advertisement', backref='user')

    def __str__(self):
        return '<User {}>'.format(self.username)

    def __repr__(self):
        return str(self)

    def set_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            "email": self.email
        }


class Advertisement(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(256))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def verify_user(self):
        print('not decorator')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title
        }