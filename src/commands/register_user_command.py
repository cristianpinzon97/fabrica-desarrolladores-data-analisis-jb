from typing import Optional, Tuple

from src.extensions import db
from src.models import User


def register_user(username: str, password: str, email: Optional[str] = None) -> Tuple[Optional[User], Optional[str]]:
    existing = User.query.filter_by(username=username).first()
    if existing is not None:
        return None, "username_exists"
    if email:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email is not None:
            return None, "email_exists"

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None


