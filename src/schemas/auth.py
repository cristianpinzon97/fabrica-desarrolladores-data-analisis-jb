from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class RegisterBody(BaseModel):
    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")
    email: Optional[EmailStr] = Field(None, description="Email address (optional)")


class LoginBody(BaseModel):
    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")


class RegisterResponse(BaseModel):
    code: int = Field(0, description="status code")
    message: str = Field("User registered successfully", description="result message")
    data: Optional[dict] = Field(None, description="User data (id, username)")


class LoginResponse(BaseModel):
    code: int = Field(0, description="status code")
    message: str = Field("Login successful", description="result message")
    data: Optional[dict] = Field(None, description="Login data (access_token)")


class ErrorResponse(BaseModel):
    code: int = Field(-1, description="status code")
    message: str = Field("Error", description="error message")
