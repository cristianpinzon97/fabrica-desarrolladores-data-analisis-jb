from typing import Optional

from src.models import User


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    if not user.verify_password(password):
        return None
    return user


