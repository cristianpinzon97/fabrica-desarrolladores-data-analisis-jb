import os

from flask import jsonify
from werkzeug.exceptions import HTTPException

from src.errors.errors import ApiError, ValidationError


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(err):
        if isinstance(err, ApiError):
            response = {
                "msg": err.description,
                "version": os.environ.get("VERSION"),
            }
            return jsonify(response), err.code
        if isinstance(err, ValidationError):
            response = {
                "msg": getattr(err, "messages_dict", str(err)),
                "version": os.environ.get("VERSION"),
            }
            return jsonify(response), 400
        if isinstance(err, HTTPException):
            response = {
                "code": err.code,
                "name": err.name,
                "description": err.description,
                "version": os.environ.get("VERSION"),
            }
            return jsonify(response), err.code
        # fallback for other exceptions
        response = {
            "msg": str(err),
            "version": os.environ.get("VERSION"),
        }
        return jsonify(response), 500
