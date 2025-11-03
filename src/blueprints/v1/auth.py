from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_openapi3 import APIBlueprint, Tag

from src.errors.errors import ValidationError
from src.extensions import db
from src.models import User

auth_tag = Tag(name="Auth", description="User authentication and registration")

api_v1_auth = APIBlueprint("auth", __name__, url_prefix="/v1/auth")


@api_v1_auth.post("/register", tags=[auth_tag])
def register():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password")
    email = (payload.get("email") or None)

    errors = {}
    if not username:
        errors["username"] = "required"
    if not password:
        errors["password"] = "required"
    if errors:
        raise ValidationError(errors)

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"msg": "username already exists"}), 409
    if email and User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "email already exists"}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "username": user.username}), 201


@api_v1_auth.post("/login", tags=[auth_tag])
def login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        raise ValidationError({"username/password": "required"})

    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        return jsonify({"msg": "invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200
