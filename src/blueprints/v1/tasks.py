from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, Field

from src.commands.create_task_command import create_task as create_task_cmd
from src.commands.delete_task_command import delete_task as delete_task_cmd
from src.commands.update_task_command import update_task as update_task_cmd
from src.queries.get_task_query import get_task_for_user
from src.queries.list_tasks_query import list_tasks_for_user
from src.schemas.tasks import (
    TaskBody,
    TaskUpdateBody,
    TaskResponse,
    CreateTaskResponse,
    UpdateTaskResponse,
    ListTasksResponse,
    DeleteTaskResponse,
    ErrorResponse,
)

tasks_tag = Tag(name="Tasks", description="CRUD operations for tasks")

api_v1_tasks = APIBlueprint("tasks", __name__, url_prefix="/v1")


class Path(BaseModel):
    tid: int = Field(..., description='task id')


@api_v1_tasks.get("/tareas", tags=[tasks_tag], responses={200: ListTasksResponse, 400: ErrorResponse})
@jwt_required()
def list_tasks():
    """
    List tasks for the authenticated user
    ---
    Returns: 200 with a list of tasks belonging to the requester
    """
    user_id = int(get_jwt_identity())
    tasks = list_tasks_for_user(user_id)
    return ListTasksResponse(code=0, message="OK", data=[t.to_dict() for t in tasks]).model_dump(), 200


@api_v1_tasks.get("/tareas/<int:tid>", tags=[tasks_tag], responses={200: TaskResponse, 404: ErrorResponse})
@jwt_required()
def get_task(path: Path):
    """
    Get a single task by id for the authenticated user
    ---
    Returns: 200 with the task or 404 if not found
    """
    user_id = int(get_jwt_identity())
    task = get_task_for_user(user_id, path.tid)
    return TaskResponse(**task.to_dict()).model_dump(), 200


@api_v1_tasks.post("/tareas", tags=[tasks_tag], responses={201: CreateTaskResponse, 400: ErrorResponse})
@jwt_required()
def create_task(body: TaskBody):
    """
    Create a new task for the authenticated user
    ---
    Request JSON: TaskBody
    Returns: 201 with created task
    """
    user_id = int(get_jwt_identity())
    task = create_task_cmd(user_id=user_id, title=body.title, description=body.description, completed=bool(body.completed))
    return CreateTaskResponse(code=0, message="Task created", data=TaskResponse(**task.to_dict())).model_dump(), 201


@api_v1_tasks.put("/tareas/<int:tid>", tags=[tasks_tag], responses={200: UpdateTaskResponse, 400: ErrorResponse, 404: ErrorResponse})
@jwt_required()
def update_task(path: Path, body: TaskUpdateBody):
    """
    Update fields of a task for the authenticated user
    ---
    Request JSON: TaskUpdateBody
    Returns: 200 with updated task or 404 if not found
    """
    user_id = int(get_jwt_identity())
    task = get_task_for_user(user_id, path.tid)

    updates = body.model_dump(exclude_unset=True)
    updated = update_task_cmd(task, updates)
    return UpdateTaskResponse(code=0, message="Task updated", data=TaskResponse(**updated.to_dict())).model_dump(), 200


@api_v1_tasks.delete("/tareas/<int:tid>", tags=[tasks_tag], responses={200: DeleteTaskResponse, 404: ErrorResponse})
@jwt_required()
def delete_task(path: Path):
    """
    Delete a task for the authenticated user
    ---
    Returns: 200 with deletion confirmation or 404 if not found
    """
    user_id = int(get_jwt_identity())
    task = get_task_for_user(user_id, path.tid)
    delete_task_cmd(task)
    return DeleteTaskResponse(code=0, message="Task deleted", data={"id": path.tid}).model_dump(), 200
