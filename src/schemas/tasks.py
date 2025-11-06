from typing import Optional, List

from pydantic import BaseModel, Field


# Reusable description constants to avoid duplicated literal warnings
_DESCRIPTION_STATUS_CODE = "status code"
_DESCRIPTION_RESULT_MESSAGE = "result message"


class TaskBody(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the task")
    description: Optional[str] = Field(None, description="Task description")
    completed: Optional[bool] = Field(False, description="Completion status")


class TaskUpdateBody(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="Title of the task")
    description: Optional[str] = Field(None, description="Task description")
    completed: Optional[bool] = Field(None, description="Completion status")


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user_id: int


class CreateTaskResponse(BaseModel):
    code: int = Field(0, description=_DESCRIPTION_STATUS_CODE)
    message: str = Field("Task created", description=_DESCRIPTION_RESULT_MESSAGE)
    data: TaskResponse


class UpdateTaskResponse(BaseModel):
    code: int = Field(0, description=_DESCRIPTION_STATUS_CODE)
    message: str = Field("Task updated", description=_DESCRIPTION_RESULT_MESSAGE)
    data: TaskResponse


class ListTasksResponse(BaseModel):
    code: int = Field(0, description=_DESCRIPTION_STATUS_CODE)
    message: str = Field("OK", description=_DESCRIPTION_RESULT_MESSAGE)
    data: List[TaskResponse]


class DeleteTaskResponse(BaseModel):
    code: int = Field(0, description=_DESCRIPTION_STATUS_CODE)
    message: str = Field("Task deleted", description=_DESCRIPTION_RESULT_MESSAGE)
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    code: int = Field(-1, description=_DESCRIPTION_STATUS_CODE)
    message: str = Field("Error", description=_DESCRIPTION_RESULT_MESSAGE)
