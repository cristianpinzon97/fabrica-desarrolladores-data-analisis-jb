from typing import Optional

from src.extensions import db
from src.errors.errors import ConflictError
from src.models import User


def register_user(username: str, password: str, email: Optional[str] = None) -> User:
    existing = User.query.filter_by(username=username).first()
    if existing is not None:
        raise ConflictError("username already exists")
    if email:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email is not None:
            raise ConflictError("email already exists")

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


