from hashlib import sha256

from sqlalchemy.sql import func

from src.extensions import db, bcrypt as bcrypt_ext


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    tasks = db.relationship("Task", backref="user", lazy=True)

    def set_password(self, password: str) -> None:
        digest = sha256((password or "").encode("utf-8")).hexdigest()
        self.password_hash = bcrypt_ext.generate_password_hash(digest).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        digest = sha256((password or "").encode("utf-8")).hexdigest()
        return bcrypt_ext.check_password_hash(self.password_hash, digest)
