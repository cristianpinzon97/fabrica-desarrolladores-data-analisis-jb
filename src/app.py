from flask_openapi3 import OpenAPI, Info

from src.blueprints.v1.auth import api_v1_auth
from src.blueprints.v1.healt_check import api_v1_health
from src.blueprints.v1.tasks import api_v1_tasks
from src.config import BaseConfig
from src.errors.handlers import register_error_handlers
from src.config.extensions import db, jwt, bcrypt

info = Info(title="Fabrica Desarrolladores API", version="1.0",
            description="API documentation with OpenAPI 3, v1 endpoints")
app = OpenAPI(__name__, info=info)

# App configuration
app.config.from_object(BaseConfig)

# Initialize extensions
db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

# Register error handlers and blueprints
register_error_handlers(app)
app.register_api(api_v1_health)
app.register_api(api_v1_auth)
app.register_api(api_v1_tasks)


@app.before_request
def create_tables():
    # Create tables if they don't exist (no migrations as requested)
    db.create_all()


if __name__ == '__main__':
    app.run()
