from src.errors.errors import UnauthorizedError
from src.models.user import User


def authenticate_user(username: str, password: str) -> User:
    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        raise UnauthorizedError("invalid credentials")
    return user


