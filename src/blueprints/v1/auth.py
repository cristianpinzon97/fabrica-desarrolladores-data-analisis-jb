from flask_jwt_extended import create_access_token
from flask_openapi3 import APIBlueprint, Tag

from src.commands.register_user_command import register_user
from src.queries.authenticate_user_query import authenticate_user
from src.schemas.auth import RegisterBody, LoginBody, RegisterResponse, LoginResponse, ErrorResponse

auth_tag = Tag(name="Auth", description="User authentication and registration")

api_v1_auth = APIBlueprint("auth", __name__, url_prefix="/v1/auth")


@api_v1_auth.post("/register", tags=[auth_tag], responses={200: RegisterResponse, 400: ErrorResponse})
def register(body: RegisterBody):
    """
    Register a new user
    """
    user = register_user(username=body.username, password=body.password, email=body.email)
    return RegisterResponse(
        code=0,
        message="User registered successfully",
        data={"id": user.id, "username": user.username}
    ).model_dump(), 200


@api_v1_auth.post("/login", tags=[auth_tag], responses={200: LoginResponse, 401: ErrorResponse})
def login(body: LoginBody):
    """
    Authenticate a user and return JWT access token
    """
    user = authenticate_user(username=body.username, password=body.password)
    token = create_access_token(identity=str(user.id))
    return LoginResponse(
        code=0,
        message="Login successful",
        data={"access_token": token}
    ).model_dump(), 200
