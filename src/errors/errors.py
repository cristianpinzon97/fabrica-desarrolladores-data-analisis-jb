# Centralized custom error classes
class ApiError(Exception):
    code = 422
    description = "Default message"

    def __init__(self, description: str = None):
        if description is not None:
            self.description = description


class ValidationError(Exception):
    def __init__(self, messages_dict):
        self.messages_dict = messages_dict
        self.code = 400
        self.description = "Validation error"

# Add other custom error classes here as needed


class ConflictError(ApiError):
    code = 409
    description = "Conflict"


class NotFoundError(ApiError):
    code = 404
    description = "Not Found"


class UnauthorizedError(ApiError):
    code = 401
    description = "Unauthorized"
