from datetime import datetime
from config import db, ma
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, db.Sequence("seq_user_id"), primary_key=True)
    name = db.Column(db.String(32))
    login = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    token = db.Column(db.String(100))
    expiration = db.Column(db.DateTime)


class Faculty(db.Model):
    __tablename__ = "faculty"
    id = db.Column(db.Integer, db.Sequence("seq_fac_id"), primary_key=True)
    name = db.Column(db.String(32), unique=True)


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, db.Sequence("seq_tech_id"), primary_key=True)
    name = db.Column(db.String(32), unique=True)

class Auditory(db.Model):
    __tablename__ = "auditory"
    id = db.Column(db.Integer, db.Sequence("seq_aud_id"), primary_key=True)
    name = db.Column(db.String(32), unique=True)


class UserSchema(ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = User
        sqla_session = db.session
        fields = ("id", "name", "login")


class TokenSchema(ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = User
        sqla_session = db.session
        fields = ("id", "name", "login", "token")

class FacultySchema(ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Faculty
        sqla_session = db.session
        fields = ("id", "name")

class TeacherSchema(ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Teacher
        sqla_session = db.session
        fields = ("id", "name")

class AuditorySchema(ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Auditory
        sqla_session = db.session
        fields = ("id", "name")
