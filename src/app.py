from flask import Flask

from src.blueprints.healt_check import health_check_blueprint
from src.errors.handlers import register_error_handlers

app = Flask(__name__)
register_error_handlers(app)

app.register_blueprint(health_check_blueprint)

if __name__ == '__main__':
    app.run()
