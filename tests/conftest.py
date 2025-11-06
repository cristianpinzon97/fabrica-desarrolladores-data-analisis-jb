import pytest

from src.app import app as _app
from src.config.extensions import db as _db


@pytest.fixture(scope="function")
def app():
    # Use the real app but ensure a clean database for each test
    _app.config["TESTING"] = True
    # Make sure any leftover sessions are removed
    with _app.app_context():
        # Drop and recreate all tables to ensure isolation
        _db.drop_all()
        _db.create_all()
        yield _app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

