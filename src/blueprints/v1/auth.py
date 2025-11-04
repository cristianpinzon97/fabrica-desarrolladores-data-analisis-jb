from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_openapi3 import APIBlueprint, Tag

from src.errors.errors import ValidationError
from src.commands.register_user_command import register_user
from src.queries.authenticate_user_query import authenticate_user

auth_tag = Tag(name="Auth", description="User authentication and registration")

api_v1_auth = APIBlueprint("auth", __name__, url_prefix="/v1/auth")


@api_v1_auth.post("/register", tags=[auth_tag])
def register():
    """
    Register a new user
    ---
    Request JSON: {"username": str, "password": str, "email": str?}
    Returns: 201 with created user id and username, or 409 on duplicates
    """
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = (payload.get("password") or "")
    email = (payload.get("email") or None)

    errors = {}
    if not username:
        errors["username"] = "required"
    if not password:
        errors["password"] = "required"
    if errors:
        raise ValidationError(errors)

    user = register_user(username=username, password=password, email=email)
    return jsonify({"id": user.id, "username": user.username}), 201


@api_v1_auth.post("/login", tags=[auth_tag])
def login():
    """
    Authenticate user and return JWT access token
    ---
    Request JSON: {"username": str, "password": str}
    Returns: 200 with {"access_token": str} or 401 on invalid credentials
    """
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        raise ValidationError({"username/password": "required"})

    user = authenticate_user(username=username, password=password)

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200
