# Centralized custom error classes
class ApiError(Exception):
    code = 422
    description = "Default message"


class ValidationError(Exception):
    def __init__(self, messages_dict):
        self.messages_dict = messages_dict
        self.code = 400
        self.description = "Validation error"

# Add other custom error classes here as needed
