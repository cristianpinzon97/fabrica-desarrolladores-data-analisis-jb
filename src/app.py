from flask_openapi3 import OpenAPI, Info

from src.blueprints.v1.healt_check import api_v1_health
from src.errors.handlers import register_error_handlers

info = Info(title="Fabrica Desarrolladores API", version="1.0",
            description="API documentation with OpenAPI 3, v1 endpoints")
app = OpenAPI(__name__, info=info)
register_error_handlers(app)
app.register_api(api_v1_health)

if __name__ == '__main__':
    app.run()
