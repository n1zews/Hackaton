from flask import make_response, abort
from config import db
from models import User, UserSchema, TokenSchema
import hashlib
import random
from datetime import datetime


def read_all(token):
    user = User.query.filter(User.token == token).one_or_none()

    if user is not None:
        users = User.query.order_by(User.id).all()
        user_schema = UserSchema(many=True)
        data = user_schema.dump(users).data
        return data
    else:
        abort(403, f"Not allowo")

def read_one(user_id):
    user = (
        User.query.filter(User.id == user_id)
        .one_or_none()
    )

    if user is not None:
        user_schema = UserSchema()
        data = user_schema.dump(user).data
        return data
    else:
        abort(404, f"Not found id: {user_id}")

def create_token():
    return hashlib.md5(bin(random.randint(1, 10000)).encode()).hexdigest()

def token(user_id, password):
    user = User.query.filter(User.id == user_id).filter(User.password == password).one_or_none()

    if user is not None:
        user.token = create_token()

        db.session.add(user)
        db.session.commit()

        user_schema = TokenSchema()
        data = user_schema.dump(user).data
        return data
    else:
        abort(403, f"Not allowed")

def create(user):
    name = user.get("name")
    login = user.get("login")
    password = user.get("password")

    existing_user = (
        User.query.filter(User.login == login)
        .filter(User.name == name)
        .one_or_none()
    )

    if existing_user is None:
        schema = UserSchema()
        new_user = User(id=(int(User.query.all()[-1].id) + 1), name=name, login=login, password=password, token=create_token(), expiration=datetime.now())

        db.session.add(new_user)
        db.session.commit()

        data = schema.dump(new_user).data

        return data, 201
    else:
         abort(409, f"User was exist")

def update(user_id, token, user):
    update_user = User.query.filter(
        User.id == user_id
    ).filter(User.token == token).one_or_none()

    name = user.get("name")
    login = user.get("login")

    if update_user is not None:
        schema = UserSchema()
        update = User(name=name, login=login)

        update.id = update_user.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_user).data

        return data, 200
    else:
        abort(404, f"Not found id: {user_id}")

def delete(user_id, token):
    user = User.query.filter(User.id == user_id).filter(User.token == token).one_or_none()

    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return make_response(f"User {user_id} deleted", 200)
    else:
        abort(404, f"Not found id: {user_id}")

